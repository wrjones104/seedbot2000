"""One-off backfill for the shared `seedlist` Firestore collection.

Two fixes, both applied in a single pass:

1. `share_url` values written by seedbot.net's local roll were origin-relative
   (`/media/foo.zip`). Other sites read this collection and resolve those against the
   wrong origin, so they are rewritten to absolute URLs against PUBLIC_BASE_URL.
2. `source` did not exist. Rows are attributed from the legacy `server_name` signal
   plus the presence of Discord guild/channel ids. Rows that match nothing are left
   unset rather than guessed at, so a later run can revisit them once there is a
   better signal - `source` is only ever written to a doc that does not have one.

Take a Firestore export before running this against prod.
"""

from urllib.parse import urljoin, urlparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from webapp.share_urls import is_local_base_url

# Firestore allows 500 operations per batch; stay under it.
BATCH_LIMIT = 400

# Legacy `server_name` value seedbot.net's web app wrote for every web roll.
SEEDBOT_WEB_SERVER_NAME = 'WebApp'

# ff6worldscollide.com writes its own hostname into `server_name` (see ultima's
# GenerateCard). Those rows are emphatically not Discord rows.
FF6WC_HOST_SUFFIX = 'ff6worldscollide.com'


class Command(BaseCommand):
    help = (
        "Rewrites relative seedlist share_urls to absolute URLs and backfills the "
        "`source` field. Run with --dry-run first."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Print the changes that would be made without writing anything.',
        )
        parser.add_argument(
            '--page-size',
            type=int,
            default=500,
            help='Documents to read per Firestore page (default: 500).',
        )
        parser.add_argument(
            '--base-url',
            default=None,
            help=(
                'Origin to rewrite relative share_urls against, e.g. '
                'https://seedbot.net. Defaults to settings.PUBLIC_BASE_URL.'
            ),
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help=(
                'Stop after touching this many documents. Use it to commit a small '
                'first slice against prod and eyeball the result before going wide.'
            ),
        )
        parser.add_argument(
            '--allow-local-base',
            action='store_true',
            help=(
                'Permit a localhost base URL. Only meaningful when pointed at a '
                'throwaway Firestore project; seedlist is otherwise shared.'
            ),
        )

    @staticmethod
    def infer_source(data):
        """Best-effort attribution for a row written before `source` existed.

        Returns None when the row cannot be attributed with confidence. Guessing is
        worse than leaving the field empty: consumers already fall back to
        `server_name`, whereas a wrong `source` is authoritative, silently skews any
        consumer that counts or filters on it, and blocks its own correction because
        the backfill only writes to docs that have no `source` yet.
        """
        # Checked first because it is the strongest signal available. Only the Discord
        # bot records guild/channel ids; both web producers write them as None. Testing
        # it ahead of server_name also means a guild that happens to be called 'WebApp'
        # is attributed by its ids rather than by its name. DM rolls still match: they
        # carry a channel_id even though server_id is None.
        if data.get('server_id') or data.get('channel_id'):
            return 'discord'

        server_name = (data.get('server_name') or '').strip().lower()

        if server_name == SEEDBOT_WEB_SERVER_NAME.lower():
            return 'seedbot_web'

        # Matches ff6worldscollide.com and its dev subdomain.
        if server_name == FF6WC_HOST_SUFFIX or server_name.endswith('.' + FF6WC_HOST_SUFFIX):
            return 'ff6wc_web'

        return None

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        page_size = options['page_size']
        limit = options['limit']
        base_url = options['base_url'] or settings.PUBLIC_BASE_URL

        if page_size < 1:
            raise CommandError(f'--page-size must be at least 1, got: {page_size}')

        if limit is not None and limit < 1:
            raise CommandError(f'--limit must be at least 1, got: {limit}')

        parsed = urlparse(base_url)
        if parsed.scheme not in ('http', 'https') or not parsed.netloc:
            raise CommandError(f"Base URL must be an absolute http(s) URL, got: {base_url!r}")

        # seedlist is a single shared collection, and .env points GOOGLE_APPLICATION_
        # CREDENTIALS at the same service account prod uses, so a dev checkout writes
        # to the same project prod does. PUBLIC_BASE_URL defaults to localhost outside
        # prod, which would bake dead localhost URLs into every historical row - and
        # irreversibly, since the rewritten values no longer start with '/' for a
        # corrected re-run to match.
        if is_local_base_url(base_url) and not options['allow_local_base']:
            raise CommandError(
                f'Refusing to write {base_url!r} into the shared seedlist collection. '
                'Pass --base-url https://seedbot.net, or --allow-local-base if you '
                'really are pointed at a throwaway Firestore project.'
            )

        # Imported after validation so a rejected invocation never opens a client.
        from bot.utils.firestore_client import db

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - no writes will be made.'))
        self.stdout.write(f'Rewriting relative share_urls against: {base_url}')
        if limit is not None:
            self.stdout.write(f'Stopping after {limit} touched document(s).')

        collection = db.collection('seedlist')
        batch = db.batch()
        pending = 0

        scanned = 0
        url_fixed = 0
        source_set = 0
        source_skipped = 0
        docs_written = 0

        cursor = None
        reached_limit = False
        while True:
            # Order by document id so pagination is stable even for docs missing fields.
            query = collection.order_by('__name__').limit(page_size)
            if cursor is not None:
                query = query.start_after(cursor)

            page = list(query.stream())
            if not page:
                break

            for doc in page:
                scanned += 1
                data = doc.to_dict() or {}
                updates = {}

                share_url = data.get('share_url')
                if isinstance(share_url, str) and share_url.startswith('/'):
                    new_url = urljoin(base_url, share_url)
                    updates['share_url'] = new_url
                    url_fixed += 1
                    self.stdout.write(f'  [{doc.id}] share_url: {share_url} -> {new_url}')

                if not data.get('source'):
                    server_name = data.get('server_name')
                    inferred = self.infer_source(data)
                    if inferred:
                        updates['source'] = inferred
                        source_set += 1
                        self.stdout.write(
                            f'  [{doc.id}] source: (empty) -> {inferred} '
                            f'(server_name={server_name!r})'
                        )
                    else:
                        source_skipped += 1
                        self.stdout.write(
                            f'  [{doc.id}] source: (empty) -> UNKNOWN, left unset '
                            f'(server_name={server_name!r})'
                        )

                if not updates:
                    continue

                docs_written += 1
                if not dry_run:
                    batch.update(doc.reference, updates)
                    pending += 1
                    if pending >= BATCH_LIMIT:
                        batch.commit()
                        self.stdout.write(f'Committed {pending} updates.')
                        batch = db.batch()
                        pending = 0

                if limit is not None and docs_written >= limit:
                    reached_limit = True
                    break

            if reached_limit:
                self.stdout.write(
                    self.style.WARNING(f'Reached --limit {limit}; stopping early.')
                )
                break

            cursor = page[-1]
            if len(page) < page_size:
                break

        if pending and not dry_run:
            batch.commit()
            self.stdout.write(f'Committed {pending} updates.')

        summary = (
            f'Scanned {scanned} doc(s). '
            f'share_url rewrites: {url_fixed}. source backfills: {source_set}. '
            f'source left unset (unattributable): {source_skipped}. '
            f'Documents touched: {docs_written}.'
        )
        if reached_limit:
            summary += ' Stopped at --limit; re-run to continue.'
        if dry_run:
            self.stdout.write(self.style.WARNING(f'DRY RUN complete. {summary}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Backfill complete. {summary}'))

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

# Firestore allows 500 operations per batch; stay under it.
BATCH_LIMIT = 400

# Legacy `server_name` value seedbot.net's web app wrote for every web roll.
SEEDBOT_WEB_SERVER_NAME = 'WebApp'

# ff6worldscollide.com writes its own hostname into `server_name` (see ultima's
# GenerateCard). Those rows are emphatically not Discord rows.
FF6WC_HOST_SUFFIX = 'ff6worldscollide.com'

LOCAL_HOSTNAMES = {'localhost', '127.0.0.1', '::1', '0.0.0.0'}


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
        server_name = (data.get('server_name') or '').strip().lower()

        if server_name == SEEDBOT_WEB_SERVER_NAME.lower():
            return 'seedbot_web'

        # Matches ff6worldscollide.com and its dev subdomain.
        if server_name == FF6WC_HOST_SUFFIX or server_name.endswith('.' + FF6WC_HOST_SUFFIX):
            return 'ff6wc_web'

        # Only the Discord bot records guild/channel ids; both web producers write
        # them as None. This is a stronger signal than "server_name is not WebApp",
        # and it still catches DM rolls, which carry a channel_id but no guild.
        if data.get('server_id') or data.get('channel_id'):
            return 'discord'

        return None

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        page_size = options['page_size']
        base_url = options['base_url'] or settings.PUBLIC_BASE_URL

        if page_size < 1:
            raise CommandError(f'--page-size must be at least 1, got: {page_size}')

        parsed = urlparse(base_url)
        if parsed.scheme not in ('http', 'https') or not parsed.netloc:
            raise CommandError(f"Base URL must be an absolute http(s) URL, got: {base_url!r}")

        # seedlist is a single shared collection and the Firestore client resolves its
        # project from ambient ADC, so a dev checkout writes to the same place prod does.
        # PUBLIC_BASE_URL defaults to localhost outside prod, which would bake dead
        # localhost URLs into every historical row - and irreversibly, since the rewritten
        # values no longer start with '/' for a corrected re-run to match.
        if parsed.hostname in LOCAL_HOSTNAMES and not options['allow_local_base']:
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

        collection = db.collection('seedlist')
        batch = db.batch()
        pending = 0

        scanned = 0
        url_fixed = 0
        source_set = 0
        source_skipped = 0
        docs_written = 0

        cursor = None
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
                if dry_run:
                    continue

                batch.update(doc.reference, updates)
                pending += 1
                if pending >= BATCH_LIMIT:
                    batch.commit()
                    self.stdout.write(f'Committed {pending} updates.')
                    batch = db.batch()
                    pending = 0

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
        if dry_run:
            self.stdout.write(self.style.WARNING(f'DRY RUN complete. {summary}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Backfill complete. {summary}'))

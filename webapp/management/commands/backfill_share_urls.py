"""One-off backfill for the shared `seedlist` Firestore collection.

Two fixes, both applied in a single pass:

1. `share_url` values written by seedbot.net's local roll were origin-relative
   (`/media/foo.zip`). Other sites read this collection and resolve those against the
   wrong origin, so they are rewritten to absolute URLs against PUBLIC_BASE_URL.
2. `source` did not exist. Rows are attributed from the legacy `server_name` signal:
   `WebApp` means the seedbot.net web app, anything else came from the Discord bot.

Take a Firestore export before running this against prod.
"""

from urllib.parse import urljoin, urlparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# Firestore allows 500 operations per batch; stay under it.
BATCH_LIMIT = 400


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
            help='Override settings.PUBLIC_BASE_URL for the rewrite.',
        )

    def handle(self, *args, **options):
        from bot.utils.firestore_client import db

        dry_run = options['dry_run']
        page_size = options['page_size']
        base_url = options['base_url'] or settings.PUBLIC_BASE_URL

        parsed = urlparse(base_url)
        if parsed.scheme not in ('http', 'https') or not parsed.netloc:
            raise CommandError(f"Base URL must be an absolute http(s) URL, got: {base_url!r}")

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - no writes will be made.'))
        self.stdout.write(f'Rewriting relative share_urls against: {base_url}')

        collection = db.collection('seedlist')
        batch = db.batch()
        pending = 0

        scanned = 0
        url_fixed = 0
        source_set = 0
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
                    inferred = 'seedbot_web' if server_name == 'WebApp' else 'discord'
                    updates['source'] = inferred
                    source_set += 1
                    self.stdout.write(
                        f'  [{doc.id}] source: (empty) -> {inferred} '
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
            f'Documents touched: {docs_written}.'
        )
        if dry_run:
            self.stdout.write(self.style.WARNING(f'DRY RUN complete. {summary}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Backfill complete. {summary}'))

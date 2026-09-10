"""Helpers for building the `share_url` values stored in the shared seedlist.

Kept in its own module rather than in `webapp.utils` so the management command can
import it without pulling in pygsheets at import time.
"""

from urllib.parse import urljoin, urlparse

from django.conf import settings

# seedlist is a single collection shared with production, and a dev checkout points
# at the same Firestore project. An absolute localhost URL written there is dead for
# every other reader and - unlike a leading-slash path - the backfill can never match
# it to repair it, because the rewrite only targets values starting with '/'.
LOCAL_HOSTNAMES = {'localhost', '127.0.0.1', '::1', '0.0.0.0'}


def is_local_base_url(base_url):
    """True when base_url points at a developer machine rather than a public origin."""
    return urlparse(base_url or '').hostname in LOCAL_HOSTNAMES


def build_public_share_url(relative_url, base_url=None):
    """Absolute URL for storage in seedlist, or the repairable relative path.

    Falls back to the origin-relative path when there is no usable public origin to
    build against. That keeps a dev roll's stored value in the one shape the backfill
    can still correct later, instead of baking a dead localhost origin into a row that
    other sites read.
    """
    base = settings.PUBLIC_BASE_URL if base_url is None else base_url
    if not base or is_local_base_url(base):
        return relative_url
    return urljoin(base, relative_url)

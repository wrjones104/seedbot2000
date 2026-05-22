import os
import logging
from google.cloud import firestore
from django.conf import settings

logger = logging.getLogger(__name__)

# Resolve GOOGLE_APPLICATION_CREDENTIALS relative path to absolute if set
creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if creds_path and not os.path.isabs(creds_path):
    absolute_creds = str(settings.BASE_DIR / creds_path)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = absolute_creds
    logger.debug(f"Resolved GOOGLE_APPLICATION_CREDENTIALS to absolute path: {absolute_creds}")

# Global Firestore client instances relying on ADC
db = firestore.Client()
db_async = firestore.AsyncClient()

def sanitize_preset_name(name: str) -> str:
    """
    Sanitize preset names by stripping unsafe characters (< > # [ ] ? *)
    and swapping forward slashes (/) with hyphens (-).
    """
    unsafe_chars = {'<', '>', '#', '[', ']', '?', '*'}
    sanitized = "".join(c for c in name if c not in unsafe_chars)
    return sanitized.replace('/', '-')

class FirestorePresetAdapter:
    """
    Adapter class wrapping Firestore document dictionary to provide property access,
    maintaining seamless compatibility with the rest of the codebase.
    """
    def __init__(self, data: dict):
        self.preset_name = data.get("preset_name", "")
        self.creator_id = str(data.get("creator_id", ""))
        self.creator_name = data.get("creator_name", "")
        self.created_at = data.get("created_at", "")
        self.flags = data.get("flags", "")
        self.description = data.get("description", "")
        self.arguments = data.get("arguments", "")
        self.official = bool(data.get("official", False))
        self.hidden = bool(data.get("hidden", False))
        self.gen_count = int(data.get("gen_count", 0))
        self.validation_status = data.get("validation_status", "PENDING")
        self.validation_error = data.get("validation_error", None)

    @property
    def pk(self):
        return self.preset_name

def get_base_url() -> str:
    """
    Constructs a well-formed base URL from Django's ALLOWED_HOSTS.
    Filters out the wildcard '*' and defaults to '127.0.0.1:8000' for local dev.
    """
    allowed = [h for h in settings.ALLOWED_HOSTS if h != '*']
    host = allowed[0] if allowed else "127.0.0.1:8000"
    scheme = "http" if ("127.0.0.1" in host or "localhost" in host) else "https"
    return f"{scheme}://{host}"


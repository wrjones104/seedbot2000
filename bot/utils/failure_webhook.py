"""Reporting failed rolls to a private Discord channel.

Nothing here may turn a failed roll into a worse failure: every path returns
rather than raises, and an unset FAILURE_WEBHOOK_URL means the bot behaves
exactly as it did before.
"""
import logging
import re
import time

import aiohttp
import discord
from django.conf import settings

logger = logging.getLogger(__name__)

# A failing API makes every roll fail at once, so identical failures collapse
# into one post per window. Without this an outage would spend the whole
# channel rate limit reporting the same thing.
COOLDOWN_SECONDS = 60

# Signatures are derived from error text, so the tracked set would otherwise
# grow for the life of the bot process.
MAX_TRACKED = 256

# Discord rejects an embed field value over 1024 characters. The whole embed
# is capped at 6000, which the fields below cannot reach - worth re-checking
# if more are added.
_FIELD_LIMIT = 1024

# Identifiers that change on every roll and so describe the occurrence rather
# than the cause. Leaving them in a signature means no two failures ever
# collapse: generate_v1_seed mints a fresh request_id per request, and it ends
# up in api_error through ApiRollError.details().
#
# Deliberately narrow. A catch-all "long hex run" rule would also fold two
# genuinely different errors together, and these cover what the code produces.
_VOLATILE = (
    (re.compile(r"request_id=[0-9A-Za-z_-]+"), "request_id=<id>"),
    (re.compile(r"[A-Za-z]:\\[^\s'\"]*\\Temp\\[^\s'\"]*", re.IGNORECASE), "<tmp>"),
    (re.compile(r"/tmp/[^\s'\"]+"), "<tmp>"),
    (re.compile(r"\b0x[0-9a-fA-F]+\b"), "<addr>"),
)


def _signature(api_error, stderr_tail, error_type) -> str:
    """A key for the cause of a failure, not for the occurrence."""
    cause = f"{api_error or ''}|{stderr_tail or ''}"
    if not cause.strip("|"):
        # Nothing describing the cause reached us. Key on the exception type
        # instead, or every unexpected error would collapse into one.
        return f"generic:{error_type or 'unknown'}"
    for pattern, placeholder in _VOLATILE:
        cause = pattern.sub(placeholder, cause)
    return cause


class _Throttle:
    """Collapses repeats of the same failure, and forgets them again.

    An instance rather than module globals so a test gets a clean one, and so
    the tracked set stays bounded in a long-lived process.
    """

    def __init__(self, cooldown: float = COOLDOWN_SECONDS, max_tracked: int = MAX_TRACKED):
        self.cooldown = cooldown
        self.max_tracked = max_tracked
        self._last_sent: dict[str, float] = {}
        self._suppressed: dict[str, int] = {}

    def claim(self, signature: str) -> tuple[bool, int]:
        """Take the window for this signature.

        Returns (post?, how many identical failures were suppressed since the
        last post), so the post that does go out can say what it stands for.
        """
        now = time.monotonic()
        last = self._last_sent.get(signature)
        if last is not None and now - last < self.cooldown:
            self._suppressed[signature] = self._suppressed.get(signature, 0) + 1
            return False, 0

        # Read before the sweep. This signature's own window has just expired,
        # so an eviction pass would discard the very tally this post exists to
        # carry.
        suppressed = self._suppressed.pop(signature, 0)
        # Only on the posting path, so an outage does not pay for it per failure
        self._evict(now)
        self._last_sent[signature] = now
        return True, suppressed

    def release(self, signature: str, suppressed: int) -> None:
        """Give back a window whose post never landed.

        claim() only hands out a window when nothing was posted recently, so
        dropping the timestamp restores the state it found.
        """
        self._last_sent.pop(signature, None)
        if suppressed:
            self._suppressed[signature] = self._suppressed.get(signature, 0) + suppressed

    def _evict(self, now: float) -> None:
        for stale in [k for k, t in self._last_sent.items() if now - t >= self.cooldown]:
            del self._last_sent[stale]
            self._suppressed.pop(stale, None)
        while len(self._last_sent) >= self.max_tracked:
            oldest = min(self._last_sent, key=self._last_sent.get)
            del self._last_sent[oldest]
            self._suppressed.pop(oldest, None)

    def reset(self) -> None:
        self._last_sent.clear()
        self._suppressed.clear()

    @property
    def tracked(self) -> int:
        return len(self._last_sent)


_throttle = _Throttle()


def reset_throttle() -> None:
    """Drop the throttle state. For tests."""
    _throttle.reset()
    _throttle.cooldown = COOLDOWN_SECONDS


def _field(value, limit: int = _FIELD_LIMIT) -> str:
    text = str(value) if value else "n/a"
    return text if len(text) <= limit else text[:limit - 1] + "…"


def _fenced(value) -> str:
    """A code block that survives truncation with its fences intact."""
    if not value:
        return "n/a"
    # 6 for the fences, 1 for the ellipsis _field may add
    return f"```{_field(value, _FIELD_LIMIT - 7)}```"


def _build_embed(*, failure_id, command, user, guild, fork, fork_commit,
                 api_error, stderr_tail, suppressed) -> discord.Embed:
    embed = discord.Embed(
        title="Roll failed",
        description=f"Reference `{failure_id}`",
        colour=discord.Colour.red(),
    )
    embed.add_field(name="Command", value=_field(command), inline=True)
    embed.add_field(name="User", value=_field(user), inline=True)
    embed.add_field(name="Server", value=_field(guild), inline=True)
    embed.add_field(name="Fork", value=_field(f"{fork} @ {fork_commit}" if fork else None), inline=False)
    embed.add_field(name="API error", value=_field(api_error or "n/a (no API roll)"), inline=False)
    embed.add_field(name="Error", value=_fenced(stderr_tail), inline=False)
    if suppressed:
        # Counted since the previous post, which may be longer ago than the
        # cooldown if the failure did not recur straight away.
        embed.set_footer(text=f"+{suppressed} identical failures suppressed since the last report")
    return embed


async def send_failure_report(*, failure_id, command, user, guild, fork=None,
                              fork_commit=None, api_error=None, stderr_tail=None,
                              error_type=None, report_path=None) -> bool:
    """Post one failed roll to the configured webhook.

    Returns whether a post was made, which is what the tests assert on. A
    False means the webhook is unset, the failure was throttled, or posting
    failed - never that the caller should do anything differently.
    """
    url = getattr(settings, "FAILURE_WEBHOOK_URL", "")
    if not url:
        return False

    signature = _signature(api_error, stderr_tail, error_type)
    should_post, suppressed = _throttle.claim(signature)
    if not should_post:
        logger.debug(f"Failure {failure_id} not reported: identical to a recent one")
        return False

    try:
        embed = _build_embed(
            failure_id=failure_id, command=command, user=user, guild=guild,
            fork=fork, fork_commit=fork_commit, api_error=api_error,
            stderr_tail=stderr_tail, suppressed=suppressed,
        )
    except Exception:
        # Formatting touches no I/O, so this is a bug here rather than a
        # network problem, and the log should not blame the network for it.
        _throttle.release(signature, suppressed)
        logger.exception(f"Could not build the failure report for {failure_id}")
        return False

    report = None
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            webhook = discord.Webhook.from_url(url, session=session)
            kwargs = {"embed": embed, "username": "SeedBot failures"}
            if report_path:
                report = discord.File(report_path, filename=f"error-{failure_id}.txt")
                kwargs["file"] = report
            await webhook.send(**kwargs)
        return True
    except Exception:
        # The window was taken before the attempt, so give it back: a
        # transient 500 must not suppress the healthy retry behind it, nor
        # lose the count the next post is meant to stand for.
        _throttle.release(signature, suppressed)
        # The roll already failed and the user already has the report; losing
        # the notification must not add a second failure on top of it.
        logger.exception(f"Could not report failure {failure_id} to the webhook")
        return False
    finally:
        # discord.py takes over closing an uploaded file, so only an unsent
        # one still holds its handle here.
        if report is not None:
            try:
                report.close()
            except Exception:
                pass

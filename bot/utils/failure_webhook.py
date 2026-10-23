"""Reporting failed rolls to a private Discord channel.

Nothing here may turn a failed roll into a worse failure: every path returns
rather than raises, and an unset FAILURE_WEBHOOK_URL means the bot behaves
exactly as it did before.
"""
import logging
import time

import aiohttp
import discord
from django.conf import settings

logger = logging.getLogger(__name__)

# A failing API makes every roll fail at once, so identical failures collapse
# into one post per window. Without this an outage would spend the whole
# channel rate limit reporting the same thing.
COOLDOWN_SECONDS = 60

# Discord rejects an embed field value over 1024 characters.
_FIELD_LIMIT = 1024

_last_sent: dict[str, float] = {}
_suppressed: dict[str, int] = {}


def _throttle(signature: str) -> tuple[bool, int]:
    """Decide whether to post this failure.

    Returns (post?, how many identical failures were suppressed since the last
    post), so the post that does go out can say what it stands for.
    """
    now = time.monotonic()
    last = _last_sent.get(signature)
    if last is not None and now - last < COOLDOWN_SECONDS:
        _suppressed[signature] = _suppressed.get(signature, 0) + 1
        return False, 0

    _last_sent[signature] = now
    return True, _suppressed.pop(signature, 0)


def reset_throttle() -> None:
    """Drop the throttle state. For tests."""
    _last_sent.clear()
    _suppressed.clear()


def _field(value, limit: int = _FIELD_LIMIT) -> str:
    text = str(value) if value else "n/a"
    return text if len(text) <= limit else text[:limit - 1] + "…"


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
    embed.add_field(name="API error", value=_field(api_error or "n/a (local roll only)"), inline=False)
    embed.add_field(name="Randomizer", value=_field(f"```{stderr_tail}```" if stderr_tail else None), inline=False)
    if suppressed:
        embed.set_footer(text=f"+{suppressed} identical failures in the last {COOLDOWN_SECONDS}s")
    return embed


async def send_failure_report(*, failure_id, command, user, guild, fork=None,
                              fork_commit=None, api_error=None, stderr_tail=None,
                              report_path=None) -> bool:
    """Post one failed roll to the configured webhook.

    Returns whether a post was made, which is what the tests assert on. A
    False means the webhook is unset, the failure was throttled, or posting
    failed - never that the caller should do anything differently.
    """
    url = getattr(settings, "FAILURE_WEBHOOK_URL", "")
    if not url:
        return False

    # The cause, not the command: during an API outage every command fails the
    # same way and should collapse, while two different randomizer errors
    # should not.
    signature = f"{api_error or ''}|{stderr_tail or ''}"
    should_post, suppressed = _throttle(signature)
    if not should_post:
        logger.debug(f"Failure {failure_id} not reported: identical to a recent one")
        return False

    try:
        embed = _build_embed(
            failure_id=failure_id, command=command, user=user, guild=guild,
            fork=fork, fork_commit=fork_commit, api_error=api_error,
            stderr_tail=stderr_tail, suppressed=suppressed,
        )
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            webhook = discord.Webhook.from_url(url, session=session)
            kwargs = {"embed": embed, "username": "SeedBot failures"}
            if report_path:
                kwargs["file"] = discord.File(report_path, filename=f"error-{failure_id}.txt")
            await webhook.send(**kwargs)
        return True
    except Exception:
        # The roll already failed and the user already has the report; losing
        # the notification must not add a second failure on top of it.
        logger.exception(f"Could not report failure {failure_id} to the webhook")
        return False

import subprocess
import re
import shlex
import sys
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def execute_and_resolve_flags(script_path: Path, flag_string: str, max_retries: int = 10) -> str | None:
    """
    Executes arguments.py. If argparse throws a mutual exclusivity error,
    it intercepts the error, removes the earlier conflicting flag, and retries.
    """
    current_flags = shlex.split(flag_string)

    # First pass: Deduplicate flags. If the user passes the exact same flag multiple times
    # (e.g. `-sc2 umaro -sc2 strago`), argparse silently overwrites the previous value.
    # To ensure a clean output string, we explicitly remove earlier occurrences of flags.
    # Note: Some flags might allow multiple uses (e.g. action='append'), but for WC flags,
    # almost all are single-use or overwritten, so we prioritize the latest user override.
    # We will only deduplicate flags starting with '-'
    flag_indices = {}
    i = 0
    while i < len(current_flags):
        if current_flags[i].startswith('-'):
            flag_name = current_flags[i]
            if flag_name in flag_indices:
                # Remove the earlier occurrence of this flag and its arguments
                old_idx = flag_indices[flag_name]
                # Find the next flag after old_idx to know how many arguments to remove
                next_flag_idx = old_idx + 1
                while next_flag_idx < len(current_flags) and not current_flags[next_flag_idx].startswith('-'):
                    next_flag_idx += 1

                # Number of elements to remove
                num_to_remove = next_flag_idx - old_idx

                logger.info(f"Resolved duplicate flag: removing earlier {flag_name} at index {old_idx}")
                for _ in range(num_to_remove):
                    current_flags.pop(old_idx)

                # Update our current index since we removed elements before it
                i -= num_to_remove

                # Rebuild flag_indices because all indices after old_idx shifted
                flag_indices = {}
                j = 0
                while j < i:
                    if current_flags[j].startswith('-'):
                        flag_indices[current_flags[j]] = j
                    j += 1

            flag_indices[flag_name] = i
        i += 1


    for attempt in range(1, max_retries + 1):
        # We invoke the branch's arguments.py as a script to let argparse run and fail if there are issues
        # Some forks' arguments.py might need the parent directory in PYTHONPATH to resolve internal imports
        # like `from args.commands import ...`
        env = None

        # We need to supply -i /some/file to bypass the required -i argument of arguments.py
        # Otherwise argparse fails on missing -i before checking mutual exclusivity of other flags.
        cmd = [sys.executable, str(script_path.absolute()), "-i", "dummy.smc"] + current_flags
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(script_path.parent.parent.absolute()))

        # We consider a successful parsing as 0. However, many arguments.py don't actually do anything when run
        # directly, so they just exit 0, or they might print help and exit.
        # Let's check stderr for argparse errors. If no stderr or no mutual exclusion error, we assume success.

        if result.returncode == 0 and not result.stderr:
            return " ".join(shlex.quote(f) for f in current_flags)

        stderr = result.stderr

        # Look for argparse mutual exclusivity errors
        # Example: "arguments.py: error: argument -sc2/--starting-character-2: not allowed with argument -sc1/--starting-character-1"
        match = re.search(r"argument (.+?): not allowed with argument (.+)", stderr)

        if not match:
            # Check if this is an assertion error from starting_party.py
            assertion_match = re.search(r"starting_party\.py\", line .+, in process", stderr)
            if assertion_match:
                # If we have an AssertionError from starting_party.py, it likely means duplicate specific characters.
                # Find occurrences of -sc1, -sc2, -sc3, -sc4
                sc_flags = [f for f in current_flags if f in ['-sc1', '-sc2', '-sc3', '-sc4']]
                sc_values = []
                for sc_flag in sc_flags:
                    idx = current_flags.index(sc_flag)
                    if idx + 1 < len(current_flags) and not current_flags[idx + 1].startswith('-'):
                        sc_values.append((sc_flag, current_flags[idx + 1]))

                # Check for duplicates
                seen = set()
                duplicate_flag = None
                for flag, val in sc_values:
                    if val not in ['random', 'randomngu']:
                        if val in seen:
                            duplicate_flag = flag
                            break
                        seen.add(val)

                if duplicate_flag:
                    idx = current_flags.index(duplicate_flag)
                    logger.info(f"Resolved starting party assertion: removing {duplicate_flag}")
                    current_flags.pop(idx) # remove flag
                    if idx < len(current_flags) and not current_flags[idx].startswith('-'):
                        current_flags.pop(idx) # remove value
                    continue

            # If there's an error but it's not a mutual exclusivity error, just return the current flags
            # It could be a missing required argument (which arguments.py might not enforce directly, but just in case)
            # or some other issue. Let the actual seed generation handle it.
            logger.warning(f"Unhandled argparse error during flag resolution:\n{stderr}")
            return " ".join(shlex.quote(f) for f in current_flags)

        arg1_group = match.group(1).split('/')
        arg2_group = match.group(2).strip().split('/')

        idx1 = max((current_flags.index(f) for f in arg1_group if f in current_flags), default=-1)
        idx2 = max((current_flags.index(f) for f in arg2_group if f in current_flags), default=-1)

        if idx1 == -1 and idx2 == -1:
            logger.warning(f"Could not find either conflicting flag in the current flags: {arg1_group} vs {arg2_group}")
            return " ".join(shlex.quote(f) for f in current_flags)

        # We want to remove the *earlier* flag, preserving the later one (user override)
        flag_idx_to_remove = min(idx1, idx2) if (idx1 != -1 and idx2 != -1) else max(idx1, idx2)
        flags_before = len(current_flags)

        removed_flag = current_flags.pop(flag_idx_to_remove)
        logger.info(f"Resolved flag conflict: removing {removed_flag}")

        # Remove associated parameters for the flag we just removed.
        # We assume anything following it that doesn't start with '-' is a parameter.
        while flag_idx_to_remove < len(current_flags) and not current_flags[flag_idx_to_remove].startswith('-'):
            removed_param = current_flags.pop(flag_idx_to_remove)
            logger.info(f"  Removed associated param: {removed_param}")

        if len(current_flags) == flags_before:
            # This shouldn't happen, but prevents infinite loops
            break

    return " ".join(shlex.quote(f) for f in current_flags)

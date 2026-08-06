import subprocess
import re
import sys
import logging
from pathlib import Path
from django.conf import settings

logger = logging.getLogger(__name__)

class RollException(Exception):
    def __init__(self, msg, filename, sperror):
        self.msg = msg
        self.sperror = sperror
        self.filename = filename
        super().__init__(self.msg)

FORK_DIRECTORIES = {
    "dev": "WorldsCollide_dev",
    "new": "WorldsCollide_dev",
    "practice": "WorldsCollide_practice",
    "doors": "WorldsCollide_ruination",
    "doorslite": "WorldsCollide_ruination",
    "doorx": "WorldsCollide_ruination",
    "dungeoncrawl": "WorldsCollide_ruination",
    "maps": "WorldsCollide_ruination",
    "mapx": "WorldsCollide_ruination",
    "lg1": "WorldsCollide_location_gating1",
    "lg2": "WorldsCollide_location_gating1",
    "ws": "WorldsCollide_shuffle_by_world",
    "csi": "WorldsCollide_shuffle_by_world",
    "ruin": "WorldsCollide_ruination",
    "shoplimits": "WorldsCollide_ruination",
    "jones": "WorldsCollide_jones",
}

# Maps an argument (e.g. from a preset's argument list) to the randomizer fork
# it should be rolled/validated against. Kept here alongside FORK_DIRECTORIES so
# there is a single source of truth for fork routing.
ARG_TO_FORK_MAP = {
    "practice": "practice",
    "dungeoncrawl": "ruin", "doorslite": "ruin", "doors": "ruin",
    "doorx": "ruin", "maps": "ruin", "mapx": "ruin",
    "ruin": "ruin", "ruinhard": "ruin", "shoplimits": "ruin",
    "lg1": "lg1", "lg2": "lg1",
    "ws": "ws", "csi": "ws",
    "jones": "jones", "who": "jones", "oops": "jones",
    "dev": "dev", "new": "new",
}


def resolve_fork_dir(arguments=None, flags: str = "") -> str:
    """Return the randomizer fork *directory* name for the given arguments and
    resolved flags, mirroring the fork routing used during seed generation.

    An argument (e.g. 'ruin', 'jones') selects the fork directly; failing that,
    fork-specific flags present in the resolved flag string (``-ruin`` / ``-sli``)
    fall back to the ruination fork, matching flag_processor.apply_args.
    """
    seed_type = None
    for arg in (arguments or []):
        arg_base = arg.lower().replace("&", "").replace("=", " ").split()[0] if arg else ""
        if arg_base in ARG_TO_FORK_MAP:
            seed_type = ARG_TO_FORK_MAP[arg_base]
            break

    # Fork-specific flags passed directly in the flag string force the ruination
    # fork even when no corresponding argument was selected.
    if "-ruin" in flags or "-sli" in flags:
        seed_type = "ruin"

    return FORK_DIRECTORIES.get(seed_type, "WorldsCollide")

def generate_local_seed(flags: str, seed_type: str = None, output_dir: Path = None) -> tuple[Path, str, str]:
    """
    Generates a local seed using the appropriate WorldsCollide fork.
    This is a synchronous, blocking function.
    """
    if not output_dir:
        raise ValueError("An output directory must be specified.")

    logger.debug(f"Starting local seed generation with flags: {flags} and seed_type: {seed_type}")
    forks_path = settings.BASE_DIR / "randomizer_forks"
    
    rolldir_name = FORK_DIRECTORIES.get(seed_type, "WorldsCollide")
    rolldir_path = forks_path / rolldir_name
    logger.debug(f"Using roll directory: {rolldir_path}")

    input_smc = settings.BASE_DIR / "data" / "ff3.smc"

    temp_filename_base = f"{seed_type or 'standard'}_local_roll"
    output_smc = output_dir / f"{temp_filename_base}.smc"
    
    import shlex
    parsed_flags = shlex.split(flags)

    # Filter out -i, -o, -manifest to prevent path-based argument injection
    filtered_flags = []
    skip_next = False
    for i, flag in enumerate(parsed_flags):
        if skip_next:
            skip_next = False
            continue
        if flag in ("-i", "-o", "-manifest"):
            skip_next = True
            continue
        if flag.startswith("-i=") or flag.startswith("-o=") or flag.startswith("-manifest="):
            continue
        filtered_flags.append(flag)

    # -sli (shoplimits) currently conflicts with -s (seed) on branches that don't support it.
    # To prevent seed ID corruption (parsing -sli as -s li), we filter it out
    # for all branches except those known to support it (currently only WorldsCollide_ruination).
    if "-sli" in filtered_flags and rolldir_name != "WorldsCollide_ruination":
        filtered_flags = [f for f in filtered_flags if f != "-sli"]

    command = [
        sys.executable, "wc.py",
        "-i", str(input_smc),
        "-o", str(output_smc),
    ]
    command.extend(filtered_flags)

    try:
        result = subprocess.run(
            command, cwd=rolldir_path, capture_output=True,
            text=True, timeout=180, check=True
        )
        
        seed_match = re.search(r"^Seed\s+(.*)$", result.stdout, re.MULTILINE)
        hash_match = re.search(r"^Hash\s+(.*)$", result.stdout, re.MULTILINE)
        
        if not seed_match or not hash_match:
            error_output = f"Could not find Seed/Hash lines.\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            raise RollException("Failed to parse script output.", temp_filename_base, error_output)
        
        seed_id = seed_match.group(1).strip()
        seed_hash = hash_match.group(1).strip()
        
        final_smc_path = output_dir / f"{seed_id}.smc"
        final_log_path = output_dir / f"{seed_id}.txt"
        
        temp_log_path = output_dir / f"{temp_filename_base}.txt"

        if output_smc.exists():
            output_smc.rename(final_smc_path)
        if temp_log_path.exists():
            temp_log_path.rename(final_log_path)
            
        return final_smc_path, seed_id, seed_hash
        
    except subprocess.CalledProcessError as e:
        raise RollException("The randomizer script failed", temp_filename_base, e.stderr or e.stdout)
    except subprocess.TimeoutExpired as e:
        raise RollException("The randomizer script timed out", temp_filename_base, e.stderr or e.stdout)
    except Exception as e:
        raise e
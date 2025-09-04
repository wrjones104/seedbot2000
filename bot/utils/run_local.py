import subprocess
import re
import sys
import asyncio
from pathlib import Path
from django.conf import settings

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
    "doors": "WorldsCollide_Door_Rando",
    "doorslite": "WorldsCollide_Door_Rando",
    "doorx": "WorldsCollide_Door_Rando",
    "dungeoncrawl": "WorldsCollide_Door_Rando",
    "maps": "WorldsCollide_Door_Rando",
    "mapx": "WorldsCollide_Door_Rando",
    "lg1": "WorldsCollide_location_gating1",
    "lg2": "WorldsCollide_location_gating1",
    "ws": "WorldsCollide_shuffle_by_world",
    "csi": "WorldsCollide_shuffle_by_world",
}

async def generate_local_seed(flags: str, seed_type: str = None) -> tuple[Path, str, str]:
    """
    Generates a local seed using the appropriate WorldsCollide fork asynchronously.
    """
    forks_path = settings.BASE_DIR / "randomizer_forks"
    
    rolldir_name = FORK_DIRECTORIES.get(seed_type, "WorldsCollide")
    rolldir_path = forks_path / rolldir_name

    input_smc = settings.BASE_DIR / "data" / "ff3.smc"
    output_dir = settings.BASE_DIR / "data" / "seeds"
    output_dir.mkdir(exist_ok=True) 

    temp_filename_base = f"{seed_type or 'standard'}_local_roll"
    output_smc = output_dir / f"{temp_filename_base}.smc"
    
    command = [
        sys.executable, "wc.py",
        "-i", str(input_smc),
        "-o", str(output_smc),
    ]
    command.extend(flags.split())

    proc = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=rolldir_path
    )

    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
        stdout_str = stdout.decode('utf-8', errors='ignore')
        stderr_str = stderr.decode('utf-8', errors='ignore')

        if proc.returncode != 0:
            raise RollException("The randomizer script failed", temp_filename_base, stderr_str)
        
        seed_match = re.search(r"^Seed\s+(.*)$", stdout_str, re.MULTILINE)
        hash_match = re.search(r"^Hash\s+(.*)$", stdout_str, re.MULTILINE)
        
        if not seed_match or not hash_match:
            error_output = f"Could not find Seed/Hash lines.\n\nSTDOUT:\n{stdout_str}\n\nSTDERR:\n{stderr_str}"
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
        
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
        raise RollException("The randomizer script timed out", temp_filename_base, "Process took more than 120 seconds to execute.")
    except Exception as e:
        raise e
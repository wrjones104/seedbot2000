from pathlib import Path
from zipfile import ZipFile

def create_seed_zip(smc_path: Path, mtype: str, has_music_spoiler: bool) -> Path:
    """
    Creates a zip archive for a generated seed.

    :param smc_path: The Path object to the generated .smc file.
    :param mtype: The seed type string, used for the zip filename.
    :param has_music_spoiler: Boolean indicating if a music spoiler should be included.
    :return: The Path object to the final .zip file.
    """
    seed_id = smc_path.stem
    zip_filename = f"{mtype}_{seed_id}.zip"
    zip_path = smc_path.with_name(zip_filename)

    with ZipFile(zip_path, "w") as zf:
        # Add the main .smc file
        if smc_path.exists():
            zf.write(smc_path, arcname=f"{mtype}_{seed_id}.smc")

        # Add the standard spoiler log
        log_path = smc_path.with_suffix('.txt')
        if log_path.exists():
            zf.write(log_path, arcname=f"{mtype}_{seed_id}.txt")
        
        # Conditionally add the music spoiler log
        if has_music_spoiler:
            music_log_path = smc_path.with_name(f"{seed_id}_spoiler.txt")
            if music_log_path.exists():
                zf.write(music_log_path, arcname=f"{mtype}_{seed_id}_music_swaps.txt")
    
    return zip_path
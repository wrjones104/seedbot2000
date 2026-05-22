from pathlib import Path
from zipfile import ZipFile

def sanitize_filename(name: str) -> str:
    """
    Sanitizes a string to be a safe filename for Windows/Linux systems.
    Replaces common illegal characters: \ / : * ? " < > |
    """
    illegal_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    sanitized = name
    for char in illegal_chars:
        sanitized = sanitized.replace(char, '')
    return sanitized

def create_seed_zip(smc_path: Path, mtype: str, has_music_spoiler: bool) -> Path:
    """
    Creates a zip archive for a generated seed.

    :param smc_path: The Path object to the generated .smc file.
    :param mtype: The seed type string, used for the zip filename.
    :param has_music_spoiler: Boolean indicating if a music spoiler should be included.
    :return: The Path object to the final .zip file.
    """
    seed_id = smc_path.stem
    clean_mtype = sanitize_filename(mtype)
    zip_filename = f"{clean_mtype}_{seed_id}.zip"
    zip_path = smc_path.with_name(zip_filename)

    with ZipFile(zip_path, "w") as zf:
        # Add the main .smc file
        if smc_path.exists():
            zf.write(smc_path, arcname=f"{clean_mtype}_{seed_id}.smc")

        # Add the standard spoiler log
        log_path = smc_path.with_suffix('.txt')
        if log_path.exists():
            zf.write(log_path, arcname=f"{clean_mtype}_{seed_id}.txt")
        
        # Conditionally add the music spoiler log
        if has_music_spoiler:
            music_log_path = smc_path.with_name(f"{seed_id}_music_spoiler.txt")
            if music_log_path.exists():
                zf.write(music_log_path, arcname=f"{clean_mtype}_{seed_id}_music_swaps.txt")
    
    return zip_path
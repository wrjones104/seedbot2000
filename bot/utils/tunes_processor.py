from pathlib import Path

# --- UPDATED: Import directly from the top-level package ---
from randomizer_forks.johnnydmad.musicrandomizer import (
    process_music,
    process_formation_music_by_table,
    process_map_music,
    get_music_spoiler
)
def apply_tunes(smc_path: Path, tunes_type: str):
    """
    Reads an smc file, applies music randomization, and overwrites the file.
    Also creates a music spoiler log.
    """
    # Read the generated ROM file
    with open(smc_path, "rb") as f:
        in_rom = f.read()

    # Set options for johnnydmad based on the tunes type
    f_chaos = (tunes_type == 'ctunes')
    f_dupes = (tunes_type == 'notunes')
    kw_args = {}
    if tunes_type == 'notunes':
        kw_args["playlist_filename"] = "silence.txt"

    # Process the ROM data in memory
    out_rom = process_music(in_rom, f_chaos=f_chaos, f_dupes=f_dupes, **kw_args)
    out_rom = process_formation_music_by_table(out_rom)
    out_rom = process_map_music(out_rom)

    # Overwrite the original .smc file with the music-randomized version
    with open(smc_path, "wb") as f:
        f.write(out_rom)

    # Get the music spoiler content and write it to a new file
    music_spoiler_content = get_music_spoiler()
    spoiler_path = smc_path.with_name(f"{smc_path.stem}_spoiler.txt")
    with open(spoiler_path, "w", encoding="utf-8") as f:
        f.write(music_spoiler_content)
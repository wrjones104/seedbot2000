# bot/utils/tunes_processor.py

from pathlib import Path
from randomizer_forks.johnnydmad.musicrandomizer import (
    process_music,
    process_formation_music_by_table,
    process_map_music,
    get_music_spoiler
)

def apply_tunes(in_rom_bytes: bytes, tunes_type: str) -> tuple[bytes, str]:
    """
    Applies music randomization to ROM data in memory.
    Returns the modified ROM bytes and the music spoiler content.
    """
    # Set options for johnnydmad based on the tunes type
    f_chaos = (tunes_type == 'ctunes')
    f_dupes = (tunes_type == 'notunes')
    kw_args = {}
    if tunes_type == 'notunes':
        kw_args["playlist_filename"] = "silence.txt"

    # Process the ROM data in memory
    out_rom = process_music(in_rom_bytes, f_chaos=f_chaos, f_dupes=f_dupes, **kw_args)
    out_rom = process_formation_music_by_table(out_rom)
    out_rom = process_map_music(out_rom)

    # Get the music spoiler content
    music_spoiler_content = get_music_spoiler()

    return out_rom, music_spoiler_content
from pathlib import Path
from typing import Union

from pathlib import Path
from randomizer_forks.johnnydmad.musicrandomizer import (
    process_music,
    process_formation_music_by_table,
    process_map_music,
    get_music_spoiler
)

# --- REFACTORED FUNCTION ---
def apply_tunes(first_arg=None, tunes_type: str = None, smc_path: Union[str, Path] = None) -> tuple[bytes, str]:
    """
    Applies music randomization. Supports two modes:
    1. In-place on a file:
       apply_tunes(smc_path=seed_path, tunes_type=tunes_type)
    2. In-memory on bytes:
       apply_tunes(in_rom_bytes, tunes_type)
    """
    in_rom_bytes = None
    file_path = None

    if smc_path is not None:
        file_path = Path(smc_path)
    elif first_arg is not None:
        if isinstance(first_arg, (str, Path)):
            file_path = Path(first_arg)
        elif isinstance(first_arg, bytes):
            in_rom_bytes = first_arg

    # If we are in file mode, read the file bytes
    if file_path is not None:
        with open(file_path, 'rb') as f:
            in_rom_bytes = f.read()

    if in_rom_bytes is None:
        raise ValueError("No ROM bytes or file path provided to apply_tunes.")

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

    # If we are in file mode, write the modified bytes back to the file
    if file_path is not None:
        with open(file_path, 'wb') as f:
            f.write(out_rom)

    return out_rom, music_spoiler_content

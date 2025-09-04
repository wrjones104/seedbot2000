"""
This module handles the processing and modification of flag strings based on arguments.
"""
import random
import re
from bot import custom_sprites_portraits

# --- Constants for Zozo defaults ---
DEFAULT_CHARACTER_NAMES = [
    "TERRA", "LOCKE", "CYAN", "SHADOW", "EDGAR", "SABIN", "CELES", "STRAGO",
    "RELM", "SETZER", "MOG", "GAU", "GOGO", "UMARO"
]
DEFAULT_PORTRAITS = list(range(len(DEFAULT_CHARACTER_NAMES) + 1))
DEFAULT_SPRITES = list(range(len(DEFAULT_CHARACTER_NAMES))) + [14, 15, 18, 19, 20, 21]
DEFAULT_PALETTES = [2, 1, 4, 4, 0, 0, 0, 3, 3, 4, 5, 3, 3, 5, 1, 0, 6, 1, 0, 3]


# --- ZOZO ARGUMENT HELPERS ---

def _parse_flag_list(flagstring: str, key: str, default_list: list) -> list:
    """
    Parses a .-separated list from a flag string for a given key (e.g., -cspr).
    Returns the default list if the key is not found.
    """
    key_search = f"-{key} "
    if key_search in flagstring:
        start = flagstring.find(key_search) + len(key_search)
        end = flagstring.find(" ", start)
        if end == -1:
            end = len(flagstring)
        
        value_part = flagstring[start:end]
        if '-' in value_part:
            return default_list

        custom_list = value_part.split('.')
        try:
            return [int(item) for item in custom_list]
        except (ValueError, TypeError):
            return custom_list
            
    return default_list

def _update_flag_list(flagstring: str, key: str, new_list: list) -> str:
    """
    Updates a flag string by either adding a new key and list or replacing an existing one.
    """
    key_search = f"-{key} "
    str_list = '.'.join(map(str, new_list))
    
    if key_search not in flagstring:
        return f"{flagstring} {key_search}{str_list}"
    
    pattern = re.compile(f"(-{key} )([^-\\s]+)")
    return pattern.sub(f"\\1{str_list}", flagstring)


# --- Main Handler for the 'zozo' argument ---

def _apply_zozo_arg(flagstring: str) -> str:
    """
    Applies the Zozo effect by creating a single shuffle order and applying it
    to characters, portraits, sprites, and palettes.
    """
    # 1. Parse existing lists from the flag string or use defaults.
    char_names = _parse_flag_list(flagstring, "name", DEFAULT_CHARACTER_NAMES)
    portraits = _parse_flag_list(flagstring, "cpor", DEFAULT_PORTRAITS)
    sprites = _parse_flag_list(flagstring, "cspr", DEFAULT_SPRITES)
    palettes = _parse_flag_list(flagstring, "cspp", DEFAULT_PALETTES)

    # 2. Create a single, shuffled order of indices based on character count.
    num_chars = len(char_names)
    shuffled_indices = list(range(num_chars))
    random.shuffle(shuffled_indices)

    # 3. Apply the consistent shuffle to all lists.
    shuffled_names = [char_names[i] for i in shuffled_indices]
    
    # Only shuffle the parts of the lists that correspond to characters.
    shuffled_portraits = [portraits[i] for i in shuffled_indices[:num_chars]] + portraits[num_chars:]
    shuffled_sprites = [sprites[i] for i in shuffled_indices[:num_chars]] + sprites[num_chars:]
    shuffled_palettes = [palettes[i] for i in shuffled_indices[:num_chars]] + palettes[num_chars:]

    # 4. Update the flag string with the new, shuffled lists.
    flagstring = _update_flag_list(flagstring, "name", shuffled_names)
    flagstring = _update_flag_list(flagstring, "cpor", shuffled_portraits)
    flagstring = _update_flag_list(flagstring, "cspr", shuffled_sprites)
    flagstring = _update_flag_list(flagstring, "cspp", shuffled_palettes)

    # 5. Remove the original name display flag.
    flagstring = flagstring.replace(" -ond ", " ")
    
    return flagstring


# --- Private Helper Functions for Flag Modifications ---

def _apply_cg_arg(flagstring: str) -> str:
    return flagstring.replace(' -open ', ' -cg ').replace('-open', '-cg')

def _apply_dash_arg(flagstring: str) -> str:
    splitflags = [flag for flag in flagstring.split("-")]
    for i, flag in enumerate(splitflags):
        if flag.strip().split(" ")[0] in ("move", "as"):
            splitflags[i] = ''
    new_flagstring = "-".join(filter(None, splitflags))
    return new_flagstring + " -move bd"

def _apply_emptychests_arg(flagstring: str) -> str:
    splitflags = [flag for flag in flagstring.split("-")]
    for i, flag in enumerate(splitflags):
        if flag.strip().split(" ")[0] in ("ccsr", "ccrt", "ccrs"):
            splitflags[i] = 'cce '
    return "-".join(splitflags)

def _apply_emptyshops_arg(flagstring: str) -> str:
    splitflags = [flag for flag in flagstring.split("-")]
    for i, flag in enumerate(splitflags):
        if flag.strip().split(" ")[0] in ("sisr", "sirt"):
            splitflags[i] = 'sie '
    return "-".join(splitflags)

def _apply_fancygau_arg(flagstring: str) -> str:
    if "-cspr" in flagstring:
        parts = flagstring.split("-cspr ")
        flag_prefix = parts[0]
        sprites_and_suffix = parts[1].split(" ", 1)
        sprites = sprites_and_suffix[0]
        flag_suffix = sprites_and_suffix[1] if len(sprites_and_suffix) > 1 else ""
        sprite_list = sprites.split(".")
        if len(sprite_list) > 11:
            sprite_list[11] = "68"
            fancysprites = ".".join(sprite_list)
            return f"{flag_prefix}-cspr {fancysprites} {flag_suffix}".strip()
    return flagstring + " -cspr 0.1.2.3.4.5.6.7.8.9.10.68.12.13.14.15.18.19.20.21"

def _apply_hundo_arg(flagstring: str) -> str:
    return flagstring + " -oa 2.3.3.2.14.14.4.27.27.6.8.8"

def _apply_kupo_arg(flagstring: str) -> str:
    return (flagstring +
            " -name KUPEK.KUMAMA.KUPOP.KUSHU.KUKU.KAMOG.KURIN.KURU.KUPO.KUTAN.MOG.KUPAN.KUGOGO.KUMARO"
            " -cpor 10.10.10.10.10.10.10.10.10.10.10.10.10.10.14"
            " -cspr 10.10.10.10.10.10.10.10.10.10.10.10.10.10.82.15.10.19.20.82"
            " -cspp 5.5.5.5.5.5.5.5.5.5.5.5.5.5.1.0.6.1.0.3")

def _apply_loot_arg(flagstring: str) -> str:
    return flagstring + " -ssd 100"

def _apply_mystery_arg(flagstring: str) -> str:
    return flagstring.replace(" -hf", "") + " -hf"

def _apply_noflashes_arg(flagstring: str) -> str:
    new_flagstring = flagstring.replace(" -frm", "").replace(" -frw", "")
    return new_flagstring + " -frw -wmhc"

def _apply_nospoilers_arg(flagstring: str) -> str:
    return flagstring.replace(" -sl", "")

def _apply_objectives_arg(flagstring: str) -> str:
    return (flagstring +
            " -oa 2.5.5.1.r.1.r.1.r.1.r.1.r.1.r.1.r.1.r"
            " -oy 0.1.1.1.r -ox 0.1.1.1.r -ow 0.1.1.1.r -ov 0.1.1.1.r")

def _apply_spoilers_arg(flagstring: str) -> str:
    return flagstring.replace(" -sl", "") + " -sl"

def _apply_yeet_arg(flagstring: str) -> str:
    flags_to_remove = [
        "-ymascot", "-ycreature", "-yimperial", "-ymain",
        "-yreflect", "-ystone", "-yvxv", "-ysketch", "-yrandom", "-yremove"
    ]
    for flag in flags_to_remove:
        flagstring = flagstring.replace(f" {flag}", "")
    return flagstring + " -yremove"

def _apply_doors_arg(flagstring: str) -> str:
    return flagstring.replace('-cg', '-open') + " -dra"

def _apply_dungeoncrawl_arg(flagstring: str) -> str:
    return flagstring.replace('-cg', '-open') + " -drdc"

def _apply_doorslite_arg(flagstring: str) -> str:
    return flagstring.replace('-cg', '-open') + " -dre"

def _apply_doorx_arg(flagstring: str) -> str:
    return flagstring.replace('-cg', '-open') + " -doorx"

# --- Argument to Action Mapping ---

ARG_ACTION_MAP = {
    'paint': lambda flags: flags + custom_sprites_portraits.paint(),
    'palette': lambda flags: flags + custom_sprites_portraits.palette(),
    'loot': _apply_loot_arg, 'hundo': _apply_hundo_arg, 'spoilers': _apply_spoilers_arg,
    'nospoilers': _apply_nospoilers_arg, 'kupo': _apply_kupo_arg,
    'objectives': _apply_objectives_arg, 'mystery': _apply_mystery_arg,
    'maps': lambda flags: flags + " -maps", 'mapx': lambda flags: flags + " -mapx",
    'cg': _apply_cg_arg, 'dash': _apply_dash_arg, 'emptychests': _apply_emptychests_arg,
    'emptyshops': _apply_emptyshops_arg, 'fancygau': _apply_fancygau_arg,
    'noflashes': _apply_noflashes_arg, 'yeet': _apply_yeet_arg, 'zozo': _apply_zozo_arg,
    'doors': _apply_doors_arg, 'dungeoncrawl': _apply_dungeoncrawl_arg,
    'doorslite': _apply_doorslite_arg, 'doorx': _apply_doorx_arg,
    'lg1': lambda flags: flags.replace("-open", "-lg1").replace("-cg", "-lg1") + " -oi 74.1.1.11.19 -oj 74.2.2.11.31.11.36 -ok 75.1.1.11.9.11.0",
    'lg2': lambda flags: flags.replace("-open", "-lg2").replace("-cg", "-lg2") + " -oi 74.1.1.11.19 -ok 75.1.1.12.2.12.5",
    'ws': lambda flags: flags.replace("-ccsr ", "-ccswr ").replace("-sisr ", "-siswr "),
}

# --- Main Public Function ---

def apply_args(original_flags: str, arguments: list) -> str:
    if not arguments:
        return original_flags
    modified_flags = original_flags
    for arg in arguments:
        action = ARG_ACTION_MAP.get(arg.lower())
        if action:
            modified_flags = action(modified_flags)
    return modified_flags
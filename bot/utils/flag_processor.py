from bot import custom_sprites_portraits

def _apply_cg_arg(flagstring):
    return flagstring.replace(' -open ', ' -cg ').replace('-open', '-cg')

def _apply_dash_arg(flagstring):
    splitflags = [flag for flag in flagstring.split("-")]
    for flag in splitflags:
        if flag.split(" ")[0] in ("move", "as"):
            splitflags[splitflags.index(flag)] = ''
    new_flagstring = "-".join(splitflags)
    new_flagstring += " -move bd"
    return new_flagstring

def _apply_emptychests_arg(flagstring):
    splitflags = [flag for flag in flagstring.split("-")]
    for flag in splitflags:
        if flag.split(" ")[0] in ("ccsr", "ccrt", "ccrs"):
            splitflags[splitflags.index(flag)] = 'cce '
    return "-".join(splitflags)

def _apply_emptyshops_arg(flagstring):
    splitflags = [flag for flag in flagstring.split("-")]
    for flag in splitflags:
        if flag.split(" ")[0] in ("sisr", "sirt"):
            splitflags[splitflags.index(flag)] = 'sie '
    return "-".join(splitflags)

def _apply_fancygau_arg(flagstring):
    if "-cspr" in flagstring:
        sprites = flagstring.split("-cspr ")[1].split(" ")[0]
        fancysprites = ".".join(
            [
                ".".join(sprites.split(".")[0:11]),
                "68",
                ".".join(sprites.split(".")[12:20]),
            ]
        )
        flagstring = " ".join(
            [
                "".join(
                    [flagstring.split("-cspr ")[0], "-cspr ", fancysprites]
                ),
                " ".join(flagstring.split("-cspr ")[1].split(" ")[1:]),
            ]
        )
    else:
        flagstring += " -cspr 0.1.2.3.4.5.6.7.8.9.10.68.12.13.14.15.18.19.20.21"
    return flagstring

def _apply_hundo_arg(flagstring):
    return flagstring + " -oa 2.3.3.2.14.14.4.27.27.6.8.8"

def _apply_kupo_arg(flagstring):
    return flagstring + (" -name KUPEK.KUMAMA.KUPOP.KUSHU.KUKU.KAMOG.KURIN.KURU.KUPO.KUTAN.MOG.KUPAN.KUGOGO.KUMARO "
                         "-cpor 10.10.10.10.10.10.10.10.10.10.10.10.10.10.14 "
                         "-cspr 10.10.10.10.10.10.10.10.10.10.10.10.10.10.82.15.10.19.20.82 "
                         "-cspp 5.5.5.5.5.5.5.5.5.5.5.5.5.5.1.0.6.1.0.3")

def _apply_loot_arg(flagstring):
    return flagstring + " -ssd 100"

def _apply_mystery_arg(flagstring):
    return "".join([flagstring.replace(" -hf", ""), " -hf"])

def _apply_noflashes_arg(flagstring):
    new_flagstring = "".join([flagstring.replace(" -frm", "").replace(" -frw", ""), " -frw"])
    new_flagstring += " -wmhc"
    return new_flagstring

def _apply_nospoilers_arg(flagstring):
    return flagstring.replace(" -sl ", " ")

def _apply_obj_arg(flagstring):
    return flagstring + (" -oa 2.5.5.1.r.1.r.1.r.1.r.1.r.1.r.1.r.1.r -oy 0.1.1.1.r -ox 0.1.1.1.r -ow 0.1.1.1.r -ov "
                         "0.1.1.1.r")

def _apply_spoilers_arg(flagstring):
    return flagstring + " -sl"

def _apply_yeet_arg(flagstring):
    return "".join(
        [
            flagstring.replace(" -ymascot", "")
            .replace(" -ycreature", "")
            .replace(" -yimperial", "")
            .replace(" -ymain", "")
            .replace(" -yreflect", "")
            .replace(" -ystone", "")
            .replace(" -yvxv", "")
            .replace(" -ysketch", "")
            .replace(" -yrandom", "")
            .replace(" -yremove", ""),
            " -yremove",
        ]
    )

def _apply_doors_arg(flagstring):
    flagstring.replace(' -open ', ' -cg ')
    flagstring += " -dra"
    return flagstring

def _apply_dungeoncrawl_arg(flagstring):
    flagstring = flagstring.replace(' -open ', ' -cg ')
    flagstring += " -drdc"
    return flagstring

def _apply_doorslite_arg(flagstring):
    flagstring = flagstring.replace(' -open ', ' -cg ')
    flagstring += " -dre"
    return flagstring

def _apply_maps_arg(flagstring):
    flagstring = flagstring.replace(' -open ', ' -cg ')
    flagstring += " -maps"
    return flagstring

def _apply_mapx_arg(flagstring):
    flagstring = flagstring.replace(' -open ', ' -cg ')
    flagstring += " -mapx"
    return flagstring

def _apply_doorx_arg(flagstring):
    flagstring = flagstring.replace(' -open ', ' -cg ')
    flagstring += " -doorx"
    return flagstring

ARG_ACTION_MAP = {
    'cg': _apply_cg_arg,
    'dash': _apply_dash_arg,
    'emptychests': _apply_emptychests_arg,
    'emptyshops': _apply_emptyshops_arg,
    'fancygau': _apply_fancygau_arg,
    'hundo': _apply_hundo_arg,
    'kupo': _apply_kupo_arg,
    'loot': _apply_loot_arg,
    'mystery': _apply_mystery_arg,
    'noflashes': _apply_noflashes_arg,
    'nospoilers': _apply_nospoilers_arg,
    'obj': _apply_obj_arg,
    'spoilers': _apply_spoilers_arg,
    'yeet': _apply_yeet_arg,
    'paint': lambda flags: flags + custom_sprites_portraits.paint(),
    'palette': lambda flags: flags + custom_sprites_portraits.palette(),
    'doors': _apply_doors_arg,
    'dungeoncrawl': _apply_dungeoncrawl_arg,
    'doorslite': _apply_doorslite_arg,
    'maps': _apply_maps_arg,
    'mapx': _apply_mapx_arg,
    'doorx': _apply_doorx_arg,
    'lg1': lambda flags: flags.replace("-open", "-lg1").replace("-cg", "-lg1") + " -oi 74.1.1.11.19 -oj 74.2.2.11.31.11.36  -ok 75.1.1.11.9.11.0 ",
    'lg2': lambda flags: flags.replace("-open", "-lg2").replace("-cg", "-lg2") + " -oi 74.1.1.11.19 -ok 75.1.1.12.2.12.5 ",
    'ws': lambda flags: flags.replace("-ccsr ", "-ccswr ").replace("-sisr ", "-siswr "),
}

# --- Main public function ---
def apply_args(original_flags: str, arguments_list: list) -> str:
    """
    Takes an original flag string and a list of arguments,
    and returns the modified flag string.
    """
    if not arguments_list:
        return original_flags

    modified_flags = original_flags
    for arg in arguments_list:
        arg_lower = arg.lower()
        if arg_lower in ARG_ACTION_MAP:
            # Call the corresponding function from the map
            modified_flags = ARG_ACTION_MAP[arg_lower](modified_flags)
            
    return modified_flags
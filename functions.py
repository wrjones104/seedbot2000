import json
import os.path
import random
import string
import sqlite3
from bingo import steve, randomize_drops
import run_local
import datetime
import re
from johnnydmad import johnnydmad
import components.views as views
import custom_sprites_portraits
from zipfile import ZipFile
from run_local import RollException

import aiohttp
import discord
import requests
from dotenv import load_dotenv

load_dotenv()


async def generate_v1_seed(flags, seed_desc, dev):
    if dev == "dev":
        url = "https://devapi.ff6worldscollide.com/api/seed"
        if seed_desc:
            payload = json.dumps(
                {
                    "key": os.getenv("dev_api_key"),
                    "flags": flags,
                    "description": seed_desc,
                }
            )
            headers = {"Content-Type": "application/json"}
        else:
            payload = json.dumps({"key": os.getenv("dev_api_key"), "flags": flags})
            headers = {"Content-Type": "application/json"}
    else:
        url = "https://api.ff6worldscollide.com/api/seed"
        if seed_desc:
            payload = json.dumps(
                {
                    "key": os.getenv("new_api_key"),
                    "flags": flags,
                    "description": seed_desc,
                }
            )
            headers = {"Content-Type": "application/json"}
        else:
            payload = json.dumps({"key": os.getenv("new_api_key"), "flags": flags})
            headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as r:
            data = await r.json()
            if "url" not in data:
                raise KeyError(f"The website said this wasn't a valid flagset... please review.")
            return data["url"], data["hash"]


async def get_vers():
    url = "https://api.ff6worldscollide.com/api/wc"
    response = requests.request("GET", url)
    data = response.json()
    return data


async def db_con():
    con = sqlite3.connect("db/seeDBot.sqlite")
    cur = con.cursor()
    return con, cur


def init_db():
    con = sqlite3.connect("db/seeDBot.sqlite")
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS presets (preset_name TEXT PRIMARY KEY, creator_id INTEGER, creator_name TEXT, created_at TEXT, flags TEXT, description TEXT, arguments TEXT, official INTEGER, hidden INTEGER, gen_count INTEGER)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS seedlist (creator_id INTEGER, creator_name TEXT, seed_type TEXT, share_url TEXT, timestamp TEXT, server_name TEXT, server_id INTEGER, channel_name TEXT, channel_id INTEGER)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS buttons (view_id TEXT, button_name TEXT, button_id TEXT PRIMARY KEY, flags TEXT, args TEXT, ispreset INTEGER, mtype TEXT)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, bot_admin INTEGER, git_user INTEGER, race_admin INTEGER)"
    )
    con.commit()
    con.close()


async def get_user(uid):
    con, cur = await db_con()
    cur.execute("SELECT * FROM users WHERE user_id = (?)", (uid,))
    user = cur.fetchone()
    con.close()
    return user


async def add_user(uid, ba, gu, ra):
    con, cur = await db_con()
    cur.execute(
        "INSERT OR REPLACE INTO users (user_id, bot_admin, git_user, race_admin) VALUES (?, ?, ?, ?)",
        (uid, ba, gu, ra),
    )
    con.commit()
    con.close()


async def del_user(uid):
    con, cur = await db_con()
    cur.execute("DELETE FROM users WHERE user_id = (?)", (uid,))
    con.commit()
    con.close()


async def get_presets(preset):
    likepreset = re.split("[^a-zA-Z]", preset)[0][:3]
    con, cur = await db_con()
    cur.execute(
        "SELECT preset_name, flags, arguments, creator_name, description FROM presets WHERE preset_name = (?) COLLATE NOCASE",
        (preset,),
    )
    thisquery = cur.fetchone()
    cur.execute(
        "SELECT preset_name, flags, arguments FROM presets WHERE preset_name LIKE '%' || (?) || '%' COLLATE NOCASE ORDER BY gen_count DESC",
        (likepreset,),
    )
    sim = cur.fetchmany(3)
    con.close()
    return thisquery, sim


async def gen_reroll_buttons(ctx, presets, flags, args, mtype):
    viewid = datetime.datetime.now().strftime("%d%m%y%H%M%S%f")
    viewids = [viewid, viewid]
    names = ["Reroll", "Reroll with Extras"]
    if presets:
        ids = [
            f"{viewid}_Reroll_{presets[0]}",
            f"{viewid}_Reroll with Extras_{presets[0]}",
        ]
    else:
        ids = [f"{viewid}_Reroll_{mtype}", f"{viewid}_Reroll with Extras_{mtype}"]
    flags = [flags, flags]
    mtypes = [mtype, mtype]
    if args:
        bargs = ["".join(args), "".join(args)]
    else:
        bargs = (None, None)
    if presets:
        ispreset = [True, True]
    else:
        ispreset = [False, False]
    names_and_ids = list(zip(viewids, names, ids, flags, bargs, ispreset, mtypes))
    await save_buttons(names_and_ids)
    view = views.ButtonView(names_and_ids)
    return view


async def save_buttons(names_and_id):
    con, cur = await db_con()
    for view_id, name, id, flags, args, ispreset, mtype in names_and_id:
        cur.execute(
            "INSERT INTO buttons (view_id, button_name, button_id, flags, args, ispreset, mtype) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (view_id, name, id, flags, args, ispreset, mtype),
        )
        con.commit()


def get_views():
    con = sqlite3.connect("db/seeDBot.sqlite")
    cur = con.cursor()
    cur.execute("SELECT DISTINCT view_id FROM buttons")
    all_records = cur.fetchall()
    last_5000 = all_records[-5000:]
    con.close()
    return last_5000


def get_buttons(viewid):
    con = sqlite3.connect("db/seeDBot.sqlite")
    cur = con.cursor()
    cur.execute("SELECT * FROM buttons WHERE view_id = (?)", (viewid,))
    names_and_ids = cur.fetchall()
    con.close()
    if names_and_ids is None:
        return None
    return names_and_ids


async def get_button_info(button_id):
    con, cur = await db_con()
    cur.execute("SELECT * FROM buttons WHERE button_id = (?)", (button_id,))
    button_info = cur.fetchone()
    con.close()
    return button_info


async def increment_preset_count(preset):
    con, cur = await db_con()
    cur.execute(
        "SELECT gen_count FROM presets WHERE preset_name = (?) COLLATE NOCASE",
        (preset,),
    )
    count = cur.fetchone()
    cur.execute(
        "UPDATE presets SET gen_count = (?) WHERE preset_name = (?) COLLATE NOCASE",
        (count[0] + 1, preset),
    )
    con.commit()
    con.close()


async def update_seedlist(m):
    con, cur = await db_con()
    try:
        cur.execute(
            "INSERT INTO seedlist VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                m["creator_id"],
                m["creator_name"],
                m["seed_type"],
                m["share_url"],
                m["timestamp"],
                m["server_name"],
                m["server_id"],
                m["channel_name"],
                m["channel_id"],
            ),
        )
        con.commit()
        con.close()
    except Exception as e:
        print(f"Something went wrong: {e}")


async def splitargs(args):
    return " ".join(args).split("&")[1:]


async def preset_argparse(args=None):
    """Returns: 0. flagstring, 1. preset_name, 2. preset_id, 3. preset_desc, 4. preset_args, 5. official, 6. hidden"""
    if args:
        flagstring = " ".join(args.split("--flags")[1:]).split("--")[0].strip()
        preset_name = " ".join(args.split()[1:]).split("--")[0].strip()
        preset_id = preset_name.lower()
        preset_desc = " ".join(args.split("--desc")[1:]).split("--")[0].strip()
        preset_args = " ".join(args.split("--args")[1:]).split("--")[0].strip()
        official = " ".join(args.split("--official")[1:]).split("--")[0].strip()
        hidden = " ".join(args.split("--hidden")[1:]).split("--")[0].strip()
        return (
            flagstring,
            preset_name,
            preset_id,
            preset_desc,
            preset_args,
            official,
            hidden,
        )
    else:
        return None

# Function to parse the flagstring and extract custom lists
async def parse_flagstring(flagstring, key, default_list, convert_func=None):
    if f"-{key}" in flagstring:
        start = flagstring.find(f"-{key}") + len(f"-{key} ")
        end = flagstring.find(" ", start)
        if end == -1:  # If it's the last flag in the string
            end = len(flagstring)
        custom_list = flagstring[start:end].split('.')
        return [convert_func(item) if convert_func else item for item in custom_list]
    return default_list


# Function to shuffle while ensuring no element remains in its original position
async def shuffle_list(ordered_list):
    """
    Shuffle a list while ensuring no element remains in its original position.
    """
    shuffled = ordered_list[:]
    while True:
        random.shuffle(shuffled)
        if all(shuffled[i] != ordered_list[i] for i in range(len(ordered_list))):
            return shuffled


# Function to update name/cpor/cspr/cspp flag's argument with a zozo shuffled version of the flag's argument
async def zozoify_flag (flagstring, key, shuffled_list):
    if f"-{key}" not in flagstring:
        # Add the key and shuffled list to the flagstring
        flagstring += f" -{key} {'.'.join(map(str, shuffled_list))}"
    else:
        # Replace the existing key's list with the shuffled list
        start = flagstring.find(f"-{key}") + len(f"-{key} ")
        end = flagstring.find(" ", start)
        if end == -1:  # If it's the last flag
            end = len(flagstring)
        flagstring = flagstring[:start] + '.'.join(map(str, shuffled_list)) + flagstring[end:]
    return flagstring

async def argparse(ctx, flags, args=None, mtype=""):
    """Parses all arguments and returns:
    0: flagstring, 1: mtype, 2: islocal, 3: seed_desc, 4: dev, 5: filename, 6: silly, 7: jdm_spoiler, 8: localhash"""
    local_args = [
        "steve",
        "tunes",
        "ctunes",
        "notunes",
        "STEVE",
        "Tunes",
        "ChaoticTunes",
        "NoTunes",
        "doors",
        "maps",
        "mapx",
        "dungeoncrawl",
        "Doors",
        "Dungeon Crawl",
        "doors_lite",
        "Doors Lite",
        "doorx",
        "local",
        "lg1",
        "lg2",
        "ws",
        "csi"
    ]
    badflags = [
        "stesp"
    ]
    # updateflags = ["crr", "cor"]
    # changeflags = {"open": "cg ", "ccrt": "ccsr 20 ", "crsr": "crr ", "cosr": "cor "}
    silly = random.choice(
        open("db/silly_things_for_seedbot_to_say.txt").read().splitlines()
    )
    islocal = False
    filename = generate_file_name()
    seed_desc = False
    dev = False
    flagstring = flags
    steve_args = "STEVE "
    jdm_spoiler = False
    localhash = False

    # initialize practice ROM variables, add practice to list of arguments
    if mtype == "practice":
        if args:
            arglist = list(args)
            arglist.append("practice")
            args = tuple(arglist)
        else:
            args = ["practice"]

    if args:
        for x in args:
            if x.strip().casefold() in map(str.lower, local_args):
                islocal = True
                break

        for x in args:
            if x.strip().casefold() == "practice":
                islocal = True
                dev = "practice"
                if mtype != "practice":
                    mtype += "_practice"

            if x.strip().casefold() == "dev":
                dev = "dev"
                mtype += "_dev"

            if x.strip().casefold() == "paint":
                flagstring += custom_sprites_portraits.paint()
                mtype += "_paint"

            if x.strip().casefold() == "kupo":
                flagstring += (
                    " -name KUPEK.KUMAMA.KUPOP.KUSHU.KUKU.KAMOG.KURIN.KURU.KUPO.KUTAN.MOG.KUPAN.KUGOGO.KUMARO "
                    "-cpor 10.10.10.10.10.10.10.10.10.10.10.10.10.10.14 "
                    "-cspr 10.10.10.10.10.10.10.10.10.10.10.10.10.10.82.15.10.19.20.82 "
                    "-cspp 5.5.5.5.5.5.5.5.5.5.5.5.5.5.1.0.6.1.0.3"
                )
                mtype += "_kupo"

            if x.strip().casefold() == "loot":
                flagstring += " -ssd 100"
                mtype += "_loot"

            if x.strip() in ("fancygau", "FancyGau"):
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
                    flagstring += (
                        " -cspr 0.1.2.3.4.5.6.7.8.9.10.68.12.13.14.15.18.19.20.21"
                    )
                mtype += "_fancygau"

            if x.strip().casefold() == "hundo":
                flagstring += " -oa 2.3.3.2.14.14.4.27.27.6.8.8"
                mtype += "_hundo"

            if x.strip() in ("obj", "Objectives"):
                flagstring += (
                    " -oa 2.5.5.1.r.1.r.1.r.1.r.1.r.1.r.1.r.1.r -oy 0.1.1.1.r -ox 0.1.1.1.r -ow 0.1.1.1.r -ov "
                    "0.1.1.1.r "
                )
                mtype += "_obj"

            if x.strip() in ("nospoilers", "NoSpoilers"):
                flagstring = flagstring.replace(" -sl ", " ")
                mtype += "_nospoilers"

            if x.strip() in ("spoilers", "Spoilers"):
                flagstring += " -sl"
                mtype += "_spoilers"

            if x.strip() in ("noflashes", "NoFlashes"):
                flagstring = "".join(
                    [flagstring.replace(" -frm", "").replace(" -frw", ""), " -frw"]
                )
                flagstring += " -wmhc"
                mtype += "_noflashes"

            if x.strip() in ("dash", "Dash"):
                splitflags = [flag for flag in flagstring.split("-")] # Create list of flags
                for flag in splitflags:
                    if flag.split(" ")[0] in ("move", "as"):
                        splitflags[splitflags.index(flag)] = ''
                flagstring += " -move bd"
                mtype += "_dash"

            if x.strip() in ("emptyshops", "EmptyShops"):
                splitflags = [flag for flag in flagstring.split("-")] # Create list of flags
                for flag in splitflags:
                    if flag.split(" ")[0] in ("sisr", "sirt"):
                        splitflags[splitflags.index(flag)] = 'sie '
                    flagstring = "-".join(splitflags)
                mtype += ' -emptyshops'

            # if &emptychests was specified
            if x.strip() in ("emptychests", "EmptyChests"):
                splitflags = [flag for flag in flagstring.split("-")] # Create list of flags
                for flag in splitflags:
                    # if one of the chest flags are found (-ccsr, -ccrt, -ccrs)
                    if flag.split(" ")[0] in ("ccsr", "ccrt", "ccrs"):
                        #  override with Empty (-cce)
                        splitflags[splitflags.index(flag)] = 'cce '
                    flagstring = "-".join(splitflags)
                mtype += ' -emptychests'

            if x.strip().casefold() == "yeet":
                flagstring = "".join(
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
                mtype += "_yeet"

            if x.strip() in ("cg", "CG"):
                flagstring = flagstring.replace("-open", "-cg")
                mtype += "_cg"

            if x.strip().casefold() == "palette":
                flagstring += custom_sprites_portraits.palette()
                mtype += "_palette"

            if x.strip().casefold() == "mystery":
                flagstring = "".join([flagstring.replace(" -hf", ""), " -hf"])
                mtype += "_mystery"

            if x.strip().casefold() == "doors":
                if dev == "dev":
                    return await ctx.channel.send("Sorry, door rando doesn't work on dev currently")
                else:
                    flagstring = flagstring.replace("-cg ", "-open ")
                    flagstring += " -dra"
                    dev = "doors"
                    mtype += "_doors"

            if x.strip() in ("dungeoncrawl", "Dungeon Crawl"):
                if dev == "dev":
                    return await ctx.channel.send(
                        "Sorry, door rando doesn't work on dev currently"
                    )
                else:
                    flagstring = flagstring.replace("-cg ", "-open ")
                    flagstring += " -drdc"
                    dev = "doors"
                    mtype += "_dungeoncrawl"

            if x.strip() in ("doors_lite", "Doors Lite"):
                if dev == "dev":
                    return await ctx.channel.send(
                        "Sorry, door rando doesn't work on dev currently"
                    )
                else:
                    flagstring = flagstring.replace("-cg ", "-open ")
                    flagstring += " -dre"
                    dev = "doors"
                    mtype += "_doors_lite"

            if x.strip() == "maps":
                if dev == "dev":
                    return await ctx.channel.send(
                        "Sorry, door rando doesn't work on dev currently"
                    )
                else:
                    flagstring += " -maps"
                    dev = "doors"
                    mtype += "_maps"

            if x.strip() == "mapx":
                if dev == "dev":
                    return await ctx.channel.send(
                        "Sorry, door rando doesn't work on dev currently"
                    )
                else:
                    flagstring += " -mapx"
                    dev = "doors"
                    mtype += "_mapx"

            if x.strip() == "doorx":
                if dev == "dev":
                    return await ctx.channel.send(
                        "Sorry, door rando doesn't work on dev currently"
                    )
                else:
                    flagstring = flagstring.replace("-cg ", "-open ")
                    flagstring += " -drx"
                    dev = "doors"
                    mtype += "_doorx"

            if x.strip().casefold() in ("ap", "apts"):
                if "Interaction" in str(ctx):
                    user = ctx.user.display_name
                else:
                    user = ctx.author.display_name
                if x == "ap":
                    ts = "off"
                else:
                    ts = "on_with_additional_gating"
                with open("db/template.yaml") as yaml:
                    yaml_content = yaml.read()
                splitflags = [flag for flag in flagstring.split("-") if flag.split(" ")[0] not in badflags] # Create list of flags excluding all bad flags
                for flag in splitflags:
                    if flag.split(" ")[0] == "name": # Remove any spaces from names since it breaks AP generation
                        splitflags[splitflags.index(flag)] = f'name {"".join(flag.split(" ")[1:]).replace(" ","")} '
                    if flag.split(" ")[0] == "open":
                        splitflags[splitflags.index(flag)] = 'cg '
                    # if flag.split(" ")[0] in updateflags: # Change flags that have been updated since 1.2 so they will work with AP
                    #     splitflags[
                    #         splitflags.index(flag)
                    #     ] = f'{flag.split(" ")[0]} '
                    # if flag.split(" ")[0] in changeflags.keys(): # Replace unworking flags with their working counterparts
                    #     splitflags[splitflags.index(flag)] = changeflags[
                    #         flag.split(" ")[0]
                    #     ]
                flagstring = "-".join(splitflags)
                with open("db/ap.yaml", "w", encoding="utf-8") as yaml_file:
                    yaml_file.write(
                        yaml_content.replace("flags", flagstring.strip())
                        .replace("ts_option", ts)
                        .replace(
                            "Player{number}",
                            "".join([user[:12], "_WC{NUMBER}"]),
                        )
                    )
                return await ctx.channel.send(
                    file=discord.File(
                        r"db/ap.yaml",
                        filename="".join(
                            [
                                user,
                                "_WC_",
                                mtype,
                                "_",
                                filename,
                                ".yaml",
                            ]
                        ),
                    )
                )

            if x.strip().casefold() == "flagsonly":
                return await ctx.channel.send(f"```{flagstring}```")

            if "steve" in x.strip().casefold():
                try:
                    steve_args = ctx.message.content.split("steve ")[1:][0].split()[0]
                    steve_args = "".join(ch for ch in steve_args if ch.isalnum())
                except IndexError:
                    steve_args = "STEVE "
                islocal = True

            if x.strip() in ("zozo", "Zozo"):
                default_character_names = ["TERRA", "LOCKE", "CYAN", "SHADOW", "EDGAR", "SABIN",
                                           "CELES", "STRAGO", "RELM", "SETZER", "MOG", "GAU",
                                           "GOGO", "UMARO"]
                default_portraits = list(range(len(default_character_names)+1))
                default_sprites = list(range(len(default_character_names)))+[14,15,18,19,20,21]
                default_palettes = [2, 1, 4, 4, 0, 0, 0, 3, 3, 4, 5, 3, 3, 5, 1, 0, 6,
                                    1, 0, 3]

                character_names = await parse_flagstring(flagstring, "name", default_character_names)
                portraits = await parse_flagstring(flagstring, "cpor", default_portraits, int)
                sprites = await parse_flagstring(flagstring, "cspr", default_sprites, int)
                palettes = await parse_flagstring(flagstring, "cspp", default_palettes, int)

                # Shuffle indices based on the character names length
                shuffled_indices = await shuffle_list(list(range(len(character_names))))

                # Apply consistent shuffle to all lists
                shuffled_characters = [character_names[i] for i in shuffled_indices]

                # Apply the same shuffle indices to the first 14 items of sprites, portraits, and palettes
                shuffled_portraits = [portraits[i] for i in shuffled_indices[:14]] + portraits[14:]
                shuffled_sprites = [sprites[i] for i in shuffled_indices[:14]] + sprites[14:]
                shuffled_palettes = [palettes[i] for i in shuffled_indices[:14]] + palettes[14:]

                # Update flagstring
                flagstring = await zozoify_flag(flagstring, "name", shuffled_characters)
                flagstring = await zozoify_flag(flagstring, "cpor", shuffled_portraits)
                flagstring = await zozoify_flag(flagstring, "cspr", shuffled_sprites)
                flagstring = await zozoify_flag(flagstring, "cspp", shuffled_palettes)
                flagstring = flagstring.replace(" -ond ", " ") # remove original name display

                mtype += "_zozo"

            if x.startswith("desc"):
                seed_desc = " ".join(x.split()[1:])

            # if lg1 option
            if x.strip() == "lg1":
                if dev == "dev":
                    return await ctx.channel.send(
                        "Sorry, location_gating1 doesn't work on dev currently"
                    )
                # add -lg1 to flagstring & add objectives to unlock WOB & WOR
                else:
                    # replace any -open or -cg with -lg1
                    flagstring = flagstring.replace("-open", "-lg1")
                    flagstring = flagstring.replace("-cg", "-lg1")
                    # use Objective oi, oj and ok since Seedbot's other commands don't override them
                    # oi = WOR unlock at FC3
                    # oj = WOR unlock for K@N and Magitek 3
                    # ok = WOB unlock for Ancient Castle or Dream 3
                    flagstring += (
                        " -oi 74.1.1.11.19 -oj 74.2.2.11.31.11.36  -ok 75.1.1.11.9.11.0 "
                    )
                    dev = "lg1"
                    mtype += "_lg1"

            # if lg2 option
            if x.strip() == "lg2":
                if dev == "dev":
                    return await ctx.channel.send(
                        "Sorry, location_gating2 doesn't work on dev currently"
                    )
                # add -lg2 to flagstring & add objectives to unlock WOB & WOR
                else:
                    # replace any -open or -cg with -lg2
                    flagstring = flagstring.replace("-open", "-lg2")
                    flagstring = flagstring.replace("-cg", "-lg2")
                    # use Objective oi, ok since Seedbot's other commands don't override them
                    # oi = WOR unlock at FC3
                    # ok = WOB unlock for Save/Kill Cid
                    flagstring += (
                        " -oi 74.1.1.11.19 -ok 75.1.1.12.2.12.5 "
                    )
                    dev = "lg2"
                    mtype += "_lg2"

            # if ws option
            if x.strip() == "ws":
                if dev == "dev":
                    return await ctx.channel.send(
                        "Sorry, shuffle by world doesn't work on dev currently"
                    )
                else:
                    flagstring = flagstring.replace("-ccsr ", "-ccswr ")
                    flagstring = flagstring.replace("-sisr ", "-siswr ")
                    dev = "ws"
                    mtype += "_ws"

            # if csi option
            if x.strip() == "csi":
                if dev == "dev":
                    return await ctx.channel.send(
                        "Sorry, custom starting items doesn't work on dev currently"
                    )
                else:
                    # this option is to enable a flag that will need to be set else where
                    dev = "csi"
                    mtype += "_csi"

        if islocal:
            try:
                localdata = await run_local.local_wc(flagstring, dev, filename)
                localhash = localdata.decode(encoding="utf-8").split("Hash")[1].strip()
            except RollException as e:
                # print(f"{datetime.datetime.utcnow()}: {e}")
                raise

        for x in args:
            if "steve" in x.strip().casefold():
                steve.steveify(steve_args, filename)
                mtype += "_steve"

        for x in args:
            if x.strip().casefold() == "tunes":
                await johnnydmad.johnnydmad("standard", filename)
                mtype += "_tunes"
                jdm_spoiler = True
                break
            elif x.strip() in ("ctunes", "ChaoticTunes"):
                await johnnydmad.johnnydmad("chaos", filename)
                mtype += "_ctunes"
                jdm_spoiler = True
                break
            elif x.strip() in ("notunes", "NoTunes"):
                await johnnydmad.johnnydmad("silent", filename)
                mtype += "_notunes"
                jdm_spoiler = True
                break

    mkey = mtype.split("_")
    mtype = "_".join(sorted(set(mkey), key=mkey.index))
    return flagstring, mtype, islocal, seed_desc, dev, filename, silly, jdm_spoiler, localhash


def generate_file_name():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))


async def send_local_seed(
    message, silly, preset, filename, jdm_spoiler, mtype, editmsg, view, localhash
):
    try:
        directory = "WorldsCollide/seeds/"
        # create a ZipFile object
        zipObj = ZipFile(directory + filename + ".zip", "w")
        # Add multiple files to the zip
        if jdm_spoiler:
            zipObj.write(
                directory + filename + "_spoiler.txt",
                arcname=mtype + "_" + filename + "_music_swaps.txt",
            )
        zipObj.write(
            directory + filename + ".smc", arcname=mtype + "_" + filename + ".smc"
        )
        zipObj.write(
            directory + filename + ".txt", arcname=mtype + "_" + filename + ".txt"
        )
        # close the Zip File
        zipObj.close()
        zipfilename = mtype + "_" + filename + ".zip"
        if "preset" in mtype:
            await editmsg.edit(
                content=f"Here's your preset seed - {silly}\n**Preset Name**: {preset[0]}\n**Created By**:"
                f" {preset[3]}\n**Description**:"
                f" {preset[4]}\n**Hash**: {localhash}",
                attachments=[
                    discord.File(directory + filename + ".zip", filename=zipfilename)
                ],
                view=view,
            )
            pass
        else:
            await editmsg.edit(
                content=f"Here's your {mtype} seed - {silly}\n**Hash**: {localhash}",
                attachments=[
                    discord.File(directory + filename + ".zip", filename=zipfilename)
                ],
                view=view,
            )
        purge_seed_files(filename, directory)
    except AttributeError:
        await editmsg.edit(
            content="There was a problem generating this seed - please try again!"
        )


def purge_seed_files(f, d):
    filetypes = [".smc", ".zip", ".txt", "_spoiler.txt"]
    base = d + f
    for x in filetypes:
        file = base + x
        if os.path.isfile(file):
            os.remove(file)

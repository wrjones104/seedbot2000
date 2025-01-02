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
                raise KeyError
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
        "dungeoncrawl",
        "Doors",
        "Dungeon Crawl",
        "doors_lite",
        "Doors Lite",
        "local",
        "lg1"
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
                    flagstring += " -kprac"    

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
                flagstring = "".join(
                    [
                        flagstring.replace(" -move og", "")
                        .replace(" -move as", "")
                        .replace(" -move bd", "")
                        .replace(" -move ssbd", ""),
                        " -move bd",
                    ]
                )
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
                flagstring = flagstring.replace(" -open ", " -cg ")
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
                    # use Objective oi, oj and ok since Seedbot's other commands don't override them
                    flagstring += (
                        " -oi 74.1.1.11.19 -oj 74.2.2.11.31.11.36  -ok 75.1.1.11.9.11.0 "
                    )

        if islocal:
            try:
                localdata = await run_local.local_wc(flagstring, dev, filename)
                localhash = localdata.decode(encoding="utf-8").split("Hash")[1].strip()
            except Exception as e:
                print(f"{datetime.datetime.utcnow()}: {e}")
                raise Exception

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


async def add_preset(message, editmsg):
    flagstring = " ".join(message.content.split("--flags")[1:]).split("--")[0].strip()
    p_name = " ".join(message.content.split()[1:]).split("--")[0].strip()
    p_id = p_name.lower()
    d_name = " ".join(message.content.split("--desc")[1:]).split("--")[0].strip()
    a_name = " ".join(message.content.split("--args")[1:]).split("--")[0].strip()
    o_name = " ".join(message.content.split("--official")[1:]).split("--")[0].strip()
    h_name = " ".join(message.content.split("--hidden")[1:]).split("--")[0].strip()
    if o_name.casefold() == "true":
        user = await get_user(message.author.id)
        try:
            if user and user[3] == 1:
                official = True
            else:
                return await editmsg.edit(
                    content="Only Racebot Admins can create official presets!"
                )
        except AttributeError:
            return await editmsg.edit(
                content="Races cannot be set as `official` in DMs"
            )
    else:
        official = False
    if h_name.casefold() == "true":
        hidden = "true"
    else:
        hidden = "false"
    if "&" in flagstring:
        return await editmsg.edit(
            content="Presets don't support additional arguments. Save your preset with __FF6WC"
            " flags only__, then you can add arguments when you roll the preset with"
            " the **!preset <name>** command later."
        )
    if not p_name:
        await editmsg.edit(
            content="Please provide a name for your preset with: **!add <name> --flags <flags> "
            "[--desc <optional description>]**"
        )
    else:
        if len(p_name) > 64:
            return await editmsg.edit(
                content="That name is too long! Make sure it's less than 64 characters!"
            )
        if not os.path.exists("db/user_presets.json"):
            with open("db/user_presets.json", "w") as newfile:
                newfile.write(json.dumps({}))
        with open("db/user_presets.json") as preset_file:
            preset_dict = json.load(preset_file)
        if p_id in preset_dict.keys():
            await editmsg.edit(
                content=f"Preset name already exists! Try another name or use **!update_preset"
                f" {p_name} --flags <flags> [--desc <optional description>]** to overwrite"
            )
        else:
            preset_dict[p_id] = {
                "name": p_name,
                "creator_id": message.author.id,
                "creator": message.author.name,
                "flags": flagstring,
                "description": d_name,
                "arguments": a_name.replace("&", ""),
                "official": official,
                "hidden": hidden,
            }
            with open("db/user_presets.json", "w") as updatefile:
                updatefile.write(json.dumps(preset_dict))
            await editmsg.edit(
                content=f"Preset saved successfully! Use the command **!preset {p_name}** to roll it!"
            )


async def add_preset_v2(ctx, name, flags, desc):
    p_id = name.lower()
    if "&" in flags:
        return await ctx.followup.send(
            "Presets don't support additional arguments. Save your preset with "
            "__FF6WC "
            " flags only__, then you can add arguments when you roll the preset with"
            " the **!preset <name>** command later.",
            ephemeral=True,
        )
    if not os.path.exists("db/user_presets.json"):
        with open("db/user_presets.json", "w") as newfile:
            newfile.write(json.dumps({}))
    with open("db/user_presets.json") as preset_file:
        preset_dict = json.load(preset_file)
    if p_id in preset_dict.keys():
        return await ctx.followup.send(
            "Preset name already exists! Try another name.", ephemeral=True
        )
    else:
        preset_dict[p_id] = {
            "name": name,
            "creator_id": ctx.user.id,
            "creator": ctx.user.name,
            "flags": flags,
            "description": desc,
        }
        with open("db/user_presets.json", "w") as updatefile:
            updatefile.write(json.dumps(preset_dict))
        message = (
            f"Preset saved successfully! Use the command **!preset {name}** to roll it!"
        )
    return message


async def update_preset(message, editmsg):
    if message.content == "!update":
        return await editmsg.edit(
            content="Please give me the name of your preset and at least one thing to edit, e.g. `!update superfunpreset --flags -cg -dnge`"
        )
    flagstring = " ".join(message.content.split("--flags")[1:]).split("--")[0].strip()
    p_name = " ".join(message.content.split()[1:]).split("--")[0].strip()
    p_id = p_name.lower()
    d_name = " ".join(message.content.split("--desc")[1:]).split("--")[0].strip()
    a_name = " ".join(message.content.split("--args")[1:]).split("--")[0].strip()
    o_name = " ".join(message.content.split("--official")[1:]).split("--")[0].strip()
    h_name = " ".join(message.content.split("--hidden")[1:]).split("--")[0].strip()
    plist = ""
    n = 0
    if o_name.casefold() == "true":
        user = await get_user(message.author.id)
        try:
            if user and user[3] == 1:
                official = True
            else:
                return await editmsg.edit(
                    content="Only Racebot Admins can create official presets!"
                )
        except AttributeError:
            return await editmsg.edit(
                content="Races cannot be set as `official` in DMs"
            )
    elif not o_name:
        pass
    else:
        official = False
    if h_name.casefold() == "true":
        hidden = "true"
    else:
        hidden = "false"
    if "&" in flagstring:
        return await editmsg.edit(
            content="Presets don't support additional arguments. Save your preset with __FF6WC"
            " flags only__, then you can add arguments when you roll the preset with"
            " the **!preset <name>** command later."
        )
    if not p_name:
        await editmsg.edit(
            content="Please provide a name for your preset with: **!update <name> --flags <flags> "
            "[--desc <optional description>]**"
        )
    else:
        if not os.path.exists("db/user_presets.json"):
            with open("db/user_presets.json", "w") as newfile:
                newfile.write(json.dumps({}))
        with open("db/user_presets.json") as preset_file:
            preset_dict = json.load(preset_file)
        if p_id not in preset_dict.keys():
            await editmsg.edit(content="I couldn't find a preset with that name!")
            for x, y in preset_dict.items():
                if y["creator_id"] == message.author.id:
                    n += 1
                    plist += f'{n}. {x}\nDescription: {y["description"]}\n'
            if plist:
                await editmsg.edit(
                    content=f"Here are all of the presets I have registered for"
                    f" you:\n```{plist}```"
                )
            else:
                await editmsg.edit(
                    content="I don't have any presets registered for you yet. Use **!add "
                    "<name> --flags <flags> [--desc <optional description>]** to add a"
                    " new one."
                )
        elif preset_dict[p_id]["creator_id"] == message.author.id:
            p_name = preset_dict[p_id]["name"]
            if not flagstring:
                flagstring = preset_dict[p_id]["flags"]
            if not d_name:
                d_name = preset_dict[p_id]["description"]
            if not a_name:
                try:
                    a_name = preset_dict[p_id]["arguments"]
                except KeyError:
                    preset_dict[p_id]["arguments"] = ""
            if not o_name:
                try:
                    official = preset_dict[p_id]["official"]
                except KeyError:
                    official = False
            preset_dict[p_id] = {
                "name": p_name,
                "creator_id": message.author.id,
                "creator": message.author.name,
                "flags": flagstring,
                "description": d_name,
                "arguments": a_name.replace("&", ""),
                "official": official,
                "hidden": hidden,
            }
            with open("db/user_presets.json", "w") as updatefile:
                updatefile.write(json.dumps(preset_dict))
            await editmsg.edit(
                content=f"Preset updated successfully! Use the command **!preset {p_name}** to roll it!"
            )
        else:
            await editmsg.edit(
                content="Sorry, you can't update a preset that you didn't create!"
            )


async def del_preset(message, editmsg):
    p_name = " ".join(message.content.split()[1:]).split("--flags")[0].strip()
    p_id = p_name.lower()
    plist = ""
    n = 0
    if not p_name:
        await editmsg.edit(
            content="Please provide a name for the preset to delete with: **!delete <name>**"
        )
    else:
        if not os.path.exists("db/user_presets.json"):
            with open("db/user_presets.json", "w") as newfile:
                newfile.write(json.dumps({}))
        with open("db/user_presets.json") as preset_file:
            preset_dict = json.load(preset_file)
        if p_id not in preset_dict.keys():
            await editmsg.edit(content="I couldn't find a preset with that name!")
            for x, y in preset_dict.items():
                if y["creator_id"] == message.author.id:
                    n += 1
                    plist += f"{n}. {x}\n"
            if plist:
                await editmsg.edit(
                    content=f"Here are all of the presets I have registered for"
                    f" you:\n```{plist}```"
                )
            else:
                await editmsg.edit(
                    content="I don't have any presets registered for you yet. Use **!add "
                    "<name> --flags <flags> [--desc <optional description>]** to add a"
                    " new one."
                )
        elif preset_dict[p_id]["creator_id"] == message.author.id:
            preset_dict.pop(p_id)
            with open("db/user_presets.json", "w") as updatefile:
                updatefile.write(json.dumps(preset_dict))
            await editmsg.edit(content="Preset deleted successfully!")
        else:
            await editmsg.edit(
                content="Sorry, you can't delete a preset that you didn't create!"
            )


async def my_presets(message, editmsg):
    if not os.path.exists("db/user_presets.json"):
        with open("db/user_presets.json", "w") as newfile:
            newfile.write(json.dumps({}))
    with open("db/user_presets.json") as checkfile:
        preset_dict = json.load(checkfile)
    plist = ""
    n = 0
    if any(message.author.id in d.values() for d in preset_dict.values()):
        for x, y in preset_dict.items():
            if y["creator_id"] == message.author.id:
                n += 1
                try:
                    if y["official"]:
                        plist += f'{n}. **{y["name"]}**\nDescription: *__(Official)__* {y["description"]}\n'
                    else:
                        plist += (
                            f'{n}. **{y["name"]}**\nDescription: {y["description"]}\n'
                        )
                except KeyError:
                    plist += f'{n}. **{y["name"]}**\nDescription: {y["description"]}\n'
        await editmsg.edit(
            content="Here are all of the presets I have registered for you:\n"
        )
        embed = discord.Embed()
        embed.title = f"{message.author.display_name}'s Presets"
        embed.description = plist
        try:
            await editmsg.edit(embed=embed)
        except Exception:
            with open("db/my_presets.txt", "w", encoding="utf-8") as preset_file:
                preset_file.write(plist)
            return await editmsg.edit(attachments=discord.File([r"db/my_presets.txt"]))

    else:
        await editmsg.edit(
            content="I don't have any presets registered for you yet. Use **!add "
            "<name> --flags <flags> [--desc <optional description>]** to add a"
            " new one."
        )


async def all_presets(message, editmsg):
    if not os.path.exists("db/user_presets.json"):
        return await editmsg.edit(content="There are no presets saved yet!")
    with open("db/user_presets.json") as f:
        a_presets = json.load(f)
        n_a_presets = "--------------------------------------------\n"
        for x, y in a_presets.items():
            xtitle = ""
            try:
                if y["official"]:
                    xtitle = "--(Official)-- "
            except KeyError:
                pass
            try:
                if y["hidden"] == "true":
                    flags = "Hidden"
                else:
                    flags = y["flags"]
            except KeyError:
                flags = y["flags"]
            try:
                n_a_presets += (
                    f"Title: {x}\nCreator: {y['creator']}\nDescription:"
                    f" {xtitle}{y['description']}\nFlags: {flags}\nAdditional Arguments: {y['arguments']}\n"
                    f"--------------------------------------------\n"
                )
            except KeyError:
                n_a_presets += (
                    f"Title: {x}\nCreator: {y['creator']}\nDescription:"
                    f" {xtitle}{y['description']}\nFlags: {flags}\n"
                    f"--------------------------------------------\n"
                )
        with open("db/all_presets.txt", "w", encoding="utf-8") as preset_file:
            preset_file.write(n_a_presets)
        return await editmsg.edit(
            content=f"Hey {message.author.display_name},"
            f" here are all saved presets:",
            attachments=[discord.File(r"db/all_presets.txt")],
        )


async def p_flags(message, editmsg):
    p_name = " ".join(message.content.split()[1:])
    p_id = p_name.lower()
    plist = ""
    n = 0
    if not p_name:
        await editmsg.edit(content="Please provide the name for the preset!")
    else:
        if not os.path.exists("db/user_presets.json"):
            with open("db/user_presets.json", "w") as newfile:
                newfile.write(json.dumps({}))
        with open("db/user_presets.json") as preset_file:
            preset_dict = json.load(preset_file)
        if p_id not in preset_dict.keys():
            await editmsg.edit(content="I couldn't find a preset with that name!")
            for x, y in preset_dict.items():
                if y["creator_id"] == message.author.id:
                    n += 1
                    plist += f'{n}. {y["name"]}\n'
            if plist:
                await editmsg.edit(
                    content=f"Here are all of the presets I have registered for"
                    f" you:\n```{plist}```"
                )
            else:
                await editmsg.edit(
                    content="I don't have any presets registered for you yet. Use **!add "
                    "<name> --flags <flags> [--desc <optional description>]** to add a"
                    " new one."
                )
        else:
            with open("db/user_presets.json") as checkfile:
                preset_dict = json.load(checkfile)
                preset = preset_dict[p_id]
            try:
                if preset["hidden"] == "true":
                    if message.author.id == preset["creator_id"]:
                        await message.author.send(
                            f'The flags for **{preset["name"]}** are:\n```{preset["flags"]}```'
                        )
                    return await editmsg.edit(
                        content="This is a hidden preset. If you are the author of this preset, check your DMs!"
                    )
                else:
                    await editmsg.edit(
                        content=f'The flags for **{preset["name"]}** are:\n```{preset["flags"]}```'
                    )
                try:
                    if preset["arguments"]:
                        await editmsg.edit(
                            content=f'Additional arguments:\n```{preset["arguments"]}```'
                        )
                except KeyError:
                    pass
            except KeyError:
                await editmsg.edit(
                    content=f'The flags for **{preset["name"]}** are:\n```{preset["flags"]}```'
                )
                try:
                    if preset["arguments"]:
                        await editmsg.edit(
                            content=f'Additional arguments:\n```{preset["arguments"]}```'
                        )
                except KeyError:
                    pass


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

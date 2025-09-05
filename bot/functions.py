import json
import os.path
import random
import string
import sqlite3
import datetime
import re
import aiohttp
import discord
import requests
import logging
from typing import List, Optional

from pathlib import Path
from zipfile import ZipFile
from django.conf import settings
from bot.utils import run_local
from bot.utils import flag_processor
import bot.components.views as views
from bot.utils.run_local import RollException
from bot import custom_sprites_portraits
from bot.utils.zip_seed import create_seed_zip

logger = logging.getLogger(__name__)

async def generate_v1_seed(flags, seed_desc, dev):
    if dev == "dev":
        url = "https://devapi.ff6worldscollide.com/api/seed"
        api_key = settings.DEV_API_KEY
    else:
        url = "https://api.ff6worldscollide.com/api/seed"
        api_key = settings.WC_API_KEY
        
    payload_data = {"key": api_key, "flags": flags}
    if seed_desc:
        payload_data["description"] = seed_desc
    
    payload = json.dumps(payload_data)
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
    db_path = settings.DATABASES['default']['NAME']
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    return con, cur


def init_db():
    db_path = settings.DATABASES['default']['NAME']
    con = sqlite3.connect(db_path)
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
    from webapp.models import Preset
    
    view = discord.ui.View(timeout=None)
    view_id_base = datetime.datetime.now().strftime("%d%m%y%H%M%S%f")
    button_args_str = " ".join(args) if args else ""
    is_preset = isinstance(presets, Preset)
    
    reroll_custom_id = f"{view_id_base}_Reroll"
    extras_custom_id = f"{view_id_base}_Extras"

    reroll_data = (view_id_base, "Reroll", reroll_custom_id, flags, button_args_str, is_preset, mtype)
    reroll_button = views.PersistentButton(
        label="Reroll",
        custom_id=reroll_custom_id,
        style=discord.ButtonStyle.primary
    )
    view.add_item(reroll_button)

    extras_data = (view_id_base, "Reroll with Extras", extras_custom_id, flags, button_args_str, is_preset, mtype)
    # --- FIX: Pass the arguments string to the button's constructor ---
    extras_button = views.RerollExtrasButton(
        label="Reroll with Extras",
        custom_id=extras_custom_id,
        style=discord.ButtonStyle.secondary,
        original_args=button_args_str
    )
    view.add_item(extras_button)

    buttons_to_save = [reroll_data, extras_data]
    await save_buttons(buttons_to_save)

    return view


async def save_buttons(names_and_id):
    con, cur = await db_con()
    for view_id, name, id, flags, args, ispreset, mtype in names_and_id:
        cur.execute(
            "INSERT INTO buttons (view_id, button_name, button_id, flags, args, ispreset, mtype) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (view_id, name, id, flags, args, ispreset, mtype),
        )
    con.commit()
    con.close()

def get_views(limit: int = 500):
    con = None 
    try:
        db_path = settings.DATABASES['default']['NAME']
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("""
            SELECT view_id 
            FROM buttons 
            GROUP BY view_id 
            ORDER BY MAX(rowid) DESC 
            LIMIT ?
        """, (limit,))
        
        recent_views = cur.fetchall()
        return recent_views
    finally:
        if con:
            con.close()


def get_buttons(viewid):
    db_path = settings.DATABASES['default']['NAME']
    con = sqlite3.connect(db_path)
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


async def splitargs(args):
    """
    Splits arguments from a format like ('&arg1', '&arg2') into a clean list: ['arg1', 'arg2']
    """
    joined_args = " ".join(args)
    split_list = filter(None, joined_args.split('&'))
    return [s.strip() for s in split_list]


async def argparse(ctx, flags: str, args: Optional[List[str]] = None, mtype: str = ""):
    logger.debug(f"Parsing arguments: flags={flags}, args={args}, mtype={mtype}")
    is_local = False
    filename = generate_file_name()
    seed_desc = None
    dev_type = None
    tunes_type = None
    flagstring = flags
    jdm_spoiler = False
    is_flagsonly = False
    ap_option = None
    if mtype == "practice":
        args.append('practice')

    if args:
        local_args = ["tunes", "ctunes", "notunes", "doors", "maps", "mapx", "dungeoncrawl", "doors_lite", "doorx", "local", "lg1", "lg2", "ws", "csi", "practice", "zozo"]

        for arg in args:
            arg_lower = arg.lower().replace("&", "").strip()

            if arg_lower in local_args:
                is_local = True

            if arg_lower in ("ap", "apts"):
                ap_option = "off" if arg_lower == "ap" else "on_with_additional_gating"
            elif arg_lower == "flagsonly":
                is_flagsonly = True
            elif arg_lower in ('practice', 'doors', 'dungeoncrawl', 'doorslite', 'maps', 'mapx', 'lg1', 'lg2', 'ws', 'csi', 'dev'):
                dev_type = arg_lower
            elif arg_lower in ('tunes', 'ctunes', 'notunes'):
                tunes_type = arg_lower
            elif arg_lower.startswith("desc"):
                seed_desc = " ".join(arg.split()[1:])

        flagstring = flag_processor.apply_args(flagstring, args)
        
        mtype = "_".join([mtype] + [a.lower() for a in args])
    
    jdm_spoiler = tunes_type is not None


    return {
        "flagstring": flagstring,
        "mtype": mtype,
        "is_local": is_local,
        "seed_desc": seed_desc,
        "dev_type": dev_type,
        "tunes_type": tunes_type,
        "filename": filename,
        "silly": random.choice(open(settings.BASE_DIR / "data" / "silly_things_for_seedbot_to_say.txt").read().splitlines()),
        "jdm_spoiler": jdm_spoiler,
        "is_flagsonly": is_flagsonly,
        "ap_option": ap_option
    }


def generate_file_name():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))


async def send_local_seed(silly, preset, mtype, seed_hash, seed_path, has_music_spoiler):
    from webapp.models import Preset
    
    try:
        zip_path = create_seed_zip(seed_path, mtype, has_music_spoiler)

        content = f"Here's your {mtype} seed - {silly}\n**Hash**: {seed_hash}"
        if isinstance(preset, Preset):
            content = (f"Here's your preset seed - {silly}\n"
                       f"**Preset Name**: {preset.preset_name}\n"
                       f"**Created By**: {preset.creator_name}\n"
                       f"**Description**: {preset.description}\n"
                       f"**Hash**: {seed_hash}")
        
        return content, zip_path

    except Exception as e:
        print(f"There was a problem zipping the seed file: {e}")
        return "There was a problem zipping this seed - please try again!", None


def purge_seed_files(seed_id: str, directory: Path):
    for suffix in [".smc", ".zip", ".txt", "_spoiler.txt"]:
        file_to_delete = directory / f"{seed_id}{suffix}"
        if file_to_delete.is_file():
            file_to_delete.unlink()
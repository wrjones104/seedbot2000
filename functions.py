import json
import os.path
import random
import string
import sqlite3
import datetime
import bingo
import johnnydmad
import custom_sprites_portraits
from zipfile import ZipFile

import aiohttp
import discord
import requests


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
                return KeyError(
                    f"API returned {data} for the following flagstring:\n```{flags}```"
                )
            return data["url"]


def get_vers(s):
    url = "https://api.ff6worldscollide.com/api/wc"
    response = requests.request("GET", url)
    data = response.json()
    return data


def db_con():
    con = sqlite3.connect("db/seeDBot.sqlite")
    cur = con.cursor()
    return con, cur


def init_db():
    con, cur = db_con()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS presets (preset_name TEXT PRIMARY KEY, creator_id INTEGER, creator_name TEXT, created_at TEXT, flags TEXT, description TEXT, arguments TEXT, official INTEGER, hidden INTEGER, gen_count INTEGER)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS seedlist (creator_id INTEGER, creator_name TEXT, seed_type TEXT, share_url TEXT, timestamp TEXT, server_name TEXT, server_id INTEGER, channel_name TEXT, channel_id INTEGER)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS buttons (button_name TEXT, button_id TEXT PRIMARY KEY, flags TEXT, args TEXT)"
    )
    con.commit()
    con.close()


def save_buttons(names_and_id):
    con, cur = db_con()
    for name, id, flags, args in names_and_id:
        cur.execute(
            "INSERT INTO buttons (button_name, button_id, flags, args) VALUES (?, ?, ?, ?)",
            (name, id, flags, args),
        )
        con.commit()


def get_buttons():
    con, cur = db_con()
    cur.execute("SELECT * FROM buttons")
    names_and_ids = cur.fetchall()
    if names_and_ids == None:
        return None
    con.close()
    return names_and_ids


def get_button_info(button_id):
    con, cur = db_con()
    cur.execute("SELECT * FROM buttons WHERE button_id = (?)", (button_id,))
    button_info = cur.fetchone()
    con.close()
    return button_info


def get_presets(preset):
    con, cur = db_con()
    cur.execute(
        "SELECT preset_name, flags, arguments, creator_name, description FROM presets WHERE preset_name = (?) COLLATE NOCASE",
        (preset,),
    )
    thisquery = cur.fetchone()
    cur.execute(
        "SELECT preset_name, flags, arguments FROM presets WHERE preset_name LIKE '%' || (?) || '%' COLLATE NOCASE ORDER BY gen_count DESC",
        (preset,),
    )
    sim = cur.fetchmany(3)
    con.close()
    return thisquery, sim


def increment_preset_count(preset):
    con, cur = db_con()
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
    con, cur = db_con()
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


def update_metrics(m):
    if not os.path.exists("db/metrics.json") or os.path.getsize("db/metrics.json") == 0:
        with open("db/metrics.json", "w") as new_file:
            new_file.write(json.dumps({}))
    try:
        m_data = json.load(open("db/metrics.json"))
        index = len(m_data) + 1
        m_data[index] = m
        with open("db/metrics.json", "w") as update_file:
            update_file.write(json.dumps(m_data))
    except json.JSONDecodeError as e:
        print(f"There was an issue writing to the metric file: {e}, please review {m}")


def myseeds(author):
    with open("db/metrics.json") as f:
        j = json.load(f)
        x = ""
        for k in j:
            if author.id == j[k]["creator_id"]:
                x += f'{j[k]["timestamp"]}: {j[k]["seed_type"]} @ {j[k]["share_url"]}\n'
        f.close()
        if x != "":
            with open("db/myseeds.txt", "w") as update_file:
                update_file.write(x)
            update_file.close()
            has_seeds = True
        else:
            has_seeds = False
    return has_seeds


async def add_preset(message):
    flagstring = " ".join(message.content.split("--flags")[1:]).split("--")[0].strip()
    p_name = " ".join(message.content.split()[1:]).split("--")[0].strip()
    p_id = p_name.lower()
    d_name = " ".join(message.content.split("--desc")[1:]).split("--")[0].strip()
    a_name = " ".join(message.content.split("--args")[1:]).split("--")[0].strip()
    o_name = " ".join(message.content.split("--official")[1:]).split("--")[0].strip()
    h_name = " ".join(message.content.split("--hidden")[1:]).split("--")[0].strip()
    if o_name.casefold() == "true":
        try:
            if "Racebot Admin" in str(message.author.roles):
                official = True
            else:
                return await message.channel.send(
                    "Only Racebot Admins can create official presets!"
                )
        except AttributeError:
            return await message.channel.send(
                "Races cannot be set as `official` in DMs"
            )
    else:
        official = False
    if h_name.casefold() == "true":
        hidden = True
    else:
        hidden = False
    if "&" in flagstring:
        return await message.channel.send(
            "Presets don't support additional arguments. Save your preset with __FF6WC"
            " flags only__, then you can add arguments when you roll the preset with"
            " the **!preset <name>** command later."
        )
    if not p_name:
        await message.channel.send(
            "Please provide a name for your preset with: **!add <name> --flags <flags> "
            "[--desc <optional description>]**"
        )
    else:
        if len(p_name) > 64:
            return await message.channel.send(
                "That name is too long! Make sure it's less than 64 characters!"
            )
        con, cur = db_con()
        cur.execute(
            f"SELECT preset_name FROM presets WHERE preset_name = (?) COLLATE NOCASE",
            (p_id,),
        )
        if cur.fetchone():
            return await message.channel.send(
                f"Preset name already exists! Try another name or use **!update_preset"
                f" {p_name} --flags <flags> [--desc <optional description>]** to overwrite"
            )
        else:
            cur.execute(
                "INSERT INTO presets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    p_name,
                    message.author.id,
                    message.author.name,
                    datetime.datetime.utcnow(),
                    flagstring,
                    d_name,
                    a_name.replace("&", ""),
                    official,
                    hidden,
                ),
            )
            con.commit()
            con.close()
            await message.channel.send(
                f"Preset saved successfully! Use the command **!preset {p_name}** to roll it!"
            )
        if not os.path.exists("db/user_presets.json"):
            with open("db/user_presets.json", "w") as newfile:
                newfile.write(json.dumps({}))
        with open("db/user_presets.json") as preset_file:
            preset_dict = json.load(preset_file)
        if p_id in preset_dict.keys():
            pass
            # await message.channel.send(f"Preset name already exists! Try another name or use **!update_preset"
            #                            f" {p_name} --flags <flags> [--desc <optional description>]** to overwrite")
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
            # await message.channel.send(f"Preset saved successfully! Use the command **!preset {p_name}** to roll it!")


async def update_preset(message):
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
        try:
            if "Racebot Admin" in str(message.author.roles):
                official = True
            else:
                return await message.channel.send(
                    "Only Racebot Admins can create official presets!"
                )
        except AttributeError:
            return await message.channel.send(
                "Races cannot be set as `official` in DMs"
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
        return await message.channel.send(
            "Presets don't support additional arguments. Save your preset with __FF6WC"
            " flags only__, then you can add arguments when you roll the preset with"
            " the **!preset <name>** command later."
        )
    if not p_name:
        await message.channel.send(
            "Please provide a name for your preset with: **!update <name> --flags <flags> "
            "[--desc <optional description>]**"
        )
    else:
        con, cur = db_con()
        cur.execute(
            f"SELECT preset_name, flags, description, arguments, official, hidden, creator_id FROM presets WHERE preset_name = (?) COLLATE NOCASE",
            (p_id,),
        )
        thisquery = cur.fetchone()
        cur.execute(
            "SELECT preset_name FROM presets WHERE preset_name LIKE '%' || (?) || '%' AND creator_id = (?) COLLATE NOCASE ORDER BY gen_count DESC",
            (p_id, message.author.id),
        )
        similar = cur.fetchmany(5)
        if not thisquery:
            sim = ""
            if similar:
                sim = f" Did you mean:```"
                for x in similar:
                    sim += f"\n!update {x[0]}"
                sim += "```"
            return await message.channel.send(
                f"I couldn't find a preset with that name!{sim}"
            )
        else:
            if thisquery[6] != message.author.id:
                return await message.channel.send(
                    f"Sorry, you can't update a preset that you didn't create!"
                )
            else:
                if not flagstring:
                    flagstring = thisquery[1]
                if not d_name:
                    d_name = thisquery[2]
                if not a_name:
                    a_name = thisquery[3]
                if not o_name:
                    o_name = thisquery[4]
                if not h_name:
                    h_name = thisquery[5]
                cur.execute(
                    "UPDATE presets SET flags = (?), description = (?), arguments = (?), official = (?), hidden = (?) WHERE preset_name = (?) COLLATE NOCASE",
                    (flagstring, d_name, a_name, o_name, h_name, p_id),
                )
                con.commit()
                con.close()
                await message.channel.send(f"Preset updated successfully!")
        if not os.path.exists("db/user_presets.json"):
            with open("db/user_presets.json", "w") as newfile:
                newfile.write(json.dumps({}))
        with open("db/user_presets.json") as preset_file:
            preset_dict = json.load(preset_file)
        if p_id not in preset_dict.keys():
            pass
            # await message.channel.send("I couldn't find a preset with that name!")
            # for x, y in preset_dict.items():
            #     if y["creator_id"] == message.author.id:
            #         n += 1
            #         plist += f'{n}. {x}\nDescription: {y["description"]}\n'
            # if plist:
            #     await message.channel.send(f"Here are all of the presets I have registered for"
            #                                f" you:\n```{plist}```")
            # else:
            #     await message.channel.send("I don't have any presets registered for you yet. Use **!add "
            #                                "<name> --flags <flags> [--desc <optional description>]** to add a"
            #                                " new one.")
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
            # await message.channel.send(f"Preset updated successfully! Use the command **!preset {p_name}** to roll it!")
        else:
            pass
            # await message.channel.send("Sorry, you can't update a preset that you didn't create!")


async def del_preset(message):
    p_name = " ".join(message.content.split()[1:]).split("--flags")[0].strip()
    p_id = p_name.lower()
    if not p_name:
        await message.channel.send(
            "Please provide a name for the preset to delete with: **!delete <name>**"
        )
    else:
        con, cur = db_con()
        cur.execute(
            f"SELECT preset_name, creator_id FROM presets WHERE preset_name = (?) COLLATE NOCASE",
            (p_id,),
        )
        thisquery = cur.fetchone()
        cur.execute(
            "SELECT preset_name FROM presets WHERE preset_name LIKE '%' || (?) || '%' AND creator_id = (?) COLLATE NOCASE ORDER BY gen_count DESC",
            (p_id, message.author.id),
        )
        similar = cur.fetchmany(5)
        if not thisquery:
            sim = ""
            if similar:
                sim = f" Did you mean:```"
                for x in similar:
                    sim += f"\n!delete {x[0]}"
                sim += "```"
            return await message.channel.send(
                f"I couldn't find a preset with that name!{sim}"
            )
        else:
            if thisquery[1] != message.author.id:
                return await message.channel.send(
                    f"Sorry, you can't delete a preset that you didn't create!"
                )
            else:
                cur.execute(
                    "DELETE FROM presets WHERE preset_name = (?) COLLATE NOCASE",
                    (p_id,),
                )
                con.commit()
                con.close()
                await message.channel.send(f"Preset deleted successfully!")
        if not os.path.exists("db/user_presets.json"):
            with open("db/user_presets.json", "w") as newfile:
                newfile.write(json.dumps({}))
        with open("db/user_presets.json") as preset_file:
            preset_dict = json.load(preset_file)
        if p_id not in preset_dict.keys():
            pass
            # await message.channel.send("I couldn't find a preset with that name!")
            # for x, y in preset_dict.items():
            #     if y["creator_id"] == message.author.id:
            #         n += 1
            #         plist += f'{n}. {x}\n'
            # if plist:
            #     await message.channel.send(f"Here are all of the presets I have registered for"
            #                                f" you:\n```{plist}```")
            # else:
            #     await message.channel.send("I don't have any presets registered for you yet. Use **!add "
            #                                "<name> --flags <flags> [--desc <optional description>]** to add a"
            #                                " new one.")
        elif preset_dict[p_id]["creator_id"] == message.author.id:
            preset_dict.pop(p_id)
            with open("db/user_presets.json", "w") as updatefile:
                updatefile.write(json.dumps(preset_dict))
            # await message.channel.send(f"Preset deleted successfully!")
        else:
            pass
            # await message.channel.send("Sorry, you can't delete a preset that you didn't create!")


async def my_presets(message):
    con, cur = db_con()
    cur.execute(
        "SELECT preset_name, description, official FROM presets WHERE creator_id = (?)",
        (message.author.id,),
    )
    thisquery = cur.fetchall()
    if not thisquery:
        await message.channel.send(
            "I don't have any presets registered for you yet. Use **!add "
            "<name> --flags <flags> [--desc <optional description>]** to add a"
            " new one."
        )
    else:
        plist = ""
        n = 0
        for x in thisquery:
            n += 1
            if x[2]:
                plist += f"{n}. **{x[0]}**\nDescription: *__(Official)__* {x[1]}\n"
            else:
                plist += f"{n}. **{x[0]}**\nDescription: {x[1]}\n"
        await message.channel.send(
            f"Here are all of the presets I have registered for you: \n"
        )
        embed = discord.Embed()
        embed.title = f"{message.author.display_name}'s Presets"
        embed.description = plist
        try:
            await message.channel.send(embed=embed)
        except:
            with open("db/my_presets.txt", "w", encoding="utf-8") as preset_file:
                preset_file.write(plist)
            return await message.channel.send(file=discord.File(r"db/my_presets.txt"))
    # if not os.path.exists('db/user_presets.json'):
    #     with open('db/user_presets.json', 'w') as newfile:
    #         newfile.write(json.dumps({}))
    # with open('db/user_presets.json') as checkfile:
    #     preset_dict = json.load(checkfile)
    # plist = ""
    # n = 0
    # if any(message.author.id in d.values() for d in preset_dict.values()):
    #     for x, y in preset_dict.items():
    #         if y['creator_id'] == message.author.id:
    #             n += 1
    #             try:
    #                 if y["official"]:
    #                     plist += f'{n}. **{y["name"]}**\nDescription: *__(Official)__* {y["description"]}\n'
    #                 else:
    #                     plist += f'{n}. **{y["name"]}**\nDescription: {y["description"]}\n'
    #             except KeyError:
    #                 plist += f'{n}. **{y["name"]}**\nDescription: {y["description"]}\n'
    #     await message.channel.send(f"Here are all of the presets I have registered for"
    #                                f" you:\n")
    #     embed = discord.Embed()
    #     embed.title = f'{message.author.display_name}\'s Presets'
    #     embed.description = plist
    #     try:
    #         await message.channel.send(embed=embed)
    #     except:
    #         with open("db/my_presets.txt", "w", encoding="utf-8") as preset_file:
    #             preset_file.write(plist)
    #         return await message.channel.send(file=discord.File(r'db/my_presets.txt'))
    # else:
    #     await message.channel.send("I don't have any presets registered for you yet. Use **!add "
    #                                "<name> --flags <flags> [--desc <optional description>]** to add a"
    #                                " new one.")


async def all_presets(message):
    con, cur = db_con()
    cur.execute(
        "SELECT preset_name, creator_name, flags, description, arguments, official, hidden FROM presets"
    )
    thisquery = cur.fetchall()
    n_a_presets = "--------------------------------------------\n"
    for x in thisquery:
        xtitle = ""
        if x[5]:
            xtitle = "--(Official)-- "
        if x[6]:
            flags = "Hidden"
        else:
            flags = x[2]
        n_a_presets += (
            f"Title: {x[0]}\nCreator: {x[1]}\nDescription:"
            f" {xtitle}{x[0]}\nFlags: {flags}\nAdditional Arguments: {x[4]}\n"
            f"--------------------------------------------\n"
        )
    # if not os.path.exists('db/user_presets.json'):
    #     return await message.channel.send("There are no presets saved yet!")
    # with open("db/user_presets.json") as f:
    #     a_presets = json.load(f)
    #     n_a_presets = "--------------------------------------------\n"
    #     for x, y in a_presets.items():
    #         xtitle = ""
    #         try:
    #             if y['official']:
    #                 xtitle = "--(Official)-- "
    #         except KeyError:
    #             pass
    #         try:
    #             if y['hidden'] == "true":
    #                 flags = "Hidden"
    #             else:
    #                 flags = y['flags']
    #         except KeyError:
    #             flags = y['flags']
    #         try:
    #             n_a_presets += f"Title: {x}\nCreator: {y['creator']}\nDescription:" \
    #                            f" {xtitle}{y['description']}\nFlags: {flags}\nAdditional Arguments: {y['arguments']}\n" \
    #                            f"--------------------------------------------\n"
    #         except KeyError:
    #             n_a_presets += f"Title: {x}\nCreator: {y['creator']}\nDescription:" \
    #                            f" {xtitle}{y['description']}\nFlags: {flags}\n" \
    #                            f"--------------------------------------------\n"
    with open("db/all_presets.txt", "w", encoding="utf-8") as preset_file:
        preset_file.write(n_a_presets)
    return await message.channel.send(
        f"Hey {message.author.display_name}," f" here are all saved presets:"
    )


async def p_flags(message):
    p_name = " ".join(message.content.split()[1:])
    p_id = p_name.lower()
    plist = ""
    n = 0
    if not p_name:
        await message.channel.send("Please provide the name for the preset!")
    else:
        con, cur = db_con()
        cur.execute(
            "SELECT flags, hidden, preset_name FROM presets WHERE preset_name = (?)",
            (p_name,),
        )
        thisquery = cur.fetchone()
        simcur = con.cursor()
        simcur.execute(
            "SELECT preset_name FROM presets WHERE preset_name LIKE '%' || (?) || '%' COLLATE NOCASE ORDER BY gen_count DESC",
            (p_name,),
        )
        similar = simcur.fetchmany(5)
        if not thisquery:
            sim = ""
            if similar:
                sim = f" Did you mean:```"
                for x in similar:
                    sim += f"\n!pflags {x[0]}"
                sim += "```"
            return await message.channel.send(
                f"I couldn't find a preset with that name!{sim}"
            )
        if thisquery[1]:
            return await message.channel.send(
                f"This is a hidden preset. If you are the author of this preset, check your DMs!"
            )
        else:
            return await message.channel.send(
                f"The flags for **{thisquery[2]}** are:\n```{thisquery[0]}```"
            )
        # if preset['hidden'] == "true":
        #     if message.author.id == preset['creator_id']:
        #         await message.author.send(f'The flags for **{preset["name"]}** are:\n```{preset["flags"]}```')
        #     return await message.channel.send(
        #         f'This is a hidden preset. If you are the author of this preset, check your DMs!')
        # else:
        #     await message.channel.send(f'The flags for **{preset["name"]}** are:\n```{preset["flags"]}```')
        # if not os.path.exists('db/user_presets.json'):
        #     with open('db/user_presets.json', 'w') as newfile:
        #         newfile.write(json.dumps({}))
        # with open('db/user_presets.json') as preset_file:
        #     preset_dict = json.load(preset_file)
        # if p_id not in preset_dict.keys():
        #     await message.channel.send("I couldn't find a preset with that name!")
        #     for x, y in preset_dict.items():
        #         if y["creator_id"] == message.author.id:
        #             n += 1
        #             plist += f'{n}. {y["name"]}\n'
        #     if plist:
        #         await message.channel.send(f"Here are all of the presets I have registered for"
        #                                    f" you:\n```{plist}```")
        #     else:
        #         await message.channel.send("I don't have any presets registered for you yet. Use **!add "
        #                                    "<name> --flags <flags> [--desc <optional description>]** to add a"
        #                                    " new one.")
        # else:
        #     with open('db/user_presets.json') as checkfile:
        #         preset_dict = json.load(checkfile)
        #         preset = preset_dict[p_id]
        #     try:
        #         if preset['hidden'] == "true":
        #             if message.author.id == preset['creator_id']:
        #                 await message.author.send(f'The flags for **{preset["name"]}** are:\n```{preset["flags"]}```')
        #             return await message.channel.send(
        #                 f'This is a hidden preset. If you are the author of this preset, check your DMs!')
        #         else:
        #             await message.channel.send(f'The flags for **{preset["name"]}** are:\n```{preset["flags"]}```')
        #         try:
        #             if preset["arguments"]:
        #                 await message.channel.send(f'Additional arguments:\n```{preset["arguments"]}```')
        #         except KeyError:
        #             pass
        #     except KeyError:
        #         await message.channel.send(f'The flags for **{preset["name"]}** are:\n```{preset["flags"]}```')
        #         try:
        #             if preset["arguments"]:
        #                 await message.channel.send(f'Additional arguments:\n```{preset["arguments"]}```')
        #         except KeyError:
        #             pass


def blamethebot(message):
    seedtype = random.choices(
        ["!rando", "!chaos", "!true_chaos", "!shuffle"], weights=[5, 3, 1, 15], k=1
    )
    loot_arg = random.choices(
        ["", "&loot", "&true_loot", "&all_pally", "&top_tier", "&poverty"],
        weights=[30, 4, 2, 1, 1, 2],
        k=1,
    )
    tune_arg = random.choices(["", "&tunes", "&ctunes"], weights=[20, 5, 2], k=1)
    sprite_arg = random.choices(
        ["", "&paint", "&kupo", "&palette"], weights=[20, 5, 2, 10], k=1
    )
    hundo = random.choices(["", "&hundo"], weights=[30, 1], k=1)
    steve = random.choices(["", "&steve"], weights=[40, 1], k=1)
    obj = random.choices(["", "&obj"], weights=[20, 1], k=1)
    nsl = random.choices(["", "&nospoiler"], weights=[10, 1], k=1)
    final_args = " ".join(
        [loot_arg[0], tune_arg[0], sprite_arg[0], hundo[0], steve[0], obj[0], nsl[0]]
    )
    desc = f"&desc Blame the Bot! Type: {''.join(seedtype[0].strip('!') + ' ' + final_args.strip().replace('&', '')).replace('  ', ' ')} - Generated by: {message.author.display_name}"
    final_msg = seedtype[0] + final_args + desc
    return final_msg, final_args


def generate_file_name():
    num1 = random.choices(
        [random.choice(string.ascii_letters), random.randint(0, 9)], k=6
    )[0]
    num2 = random.choices(
        [random.choice(string.ascii_letters), random.randint(0, 9)], k=1
    )[0]
    num3 = random.choices(
        [random.choice(string.ascii_letters), random.randint(0, 9)], k=1
    )[0]
    num4 = random.choices(
        [random.choice(string.ascii_letters), random.randint(0, 9)], k=1
    )[0]
    num5 = random.choices(
        [random.choice(string.ascii_letters), random.randint(0, 9)], k=1
    )[0]
    num6 = random.choices(
        [random.choice(string.ascii_letters), random.randint(0, 9)], k=1
    )[0]
    filename = "".join(
        [str(num1), str(num2), str(num3), str(num4), str(num5), str(num6)]
    )
    return filename


async def send_local_seed(message, silly, pcheck, views, filename, jdm_spoiler, mtype, editmsg):
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
            await message.channel.send(
                f"Here's your preset seed - {silly}\n**Preset Name**: {pcheck[0][0]}\n**Created By**:"
                f" {pcheck[0][3]}\n**Description**:"
                f" {pcheck[0][4]}",
                file=discord.File(directory + filename + ".zip", filename=zipfilename),
                view=views.ReRollView(message),
            )
        else:
            await message.chanel.send(
                f"Here's your {mtype} seed - {silly}",
                file=discord.File(directory + filename + ".zip", filename=zipfilename),
                view=views.ReRollView(message),
            )
        purge_seed_files(filename, directory)
    except AttributeError:
        await editmsg.edit(content=
            "There was a problem generating this seed - please try again!"
        )


async def parse_main_args(ctx, flags, args=None):
    local_args = [
        "loot",
        "true_loot",
        "all_pally",
        "top_tier",
        "steve",
        "tunes",
        "ctunes",
        "notunes",
        "poverty",
        "Loot",
        "True Loot",
        "Poverty",
        "STEVE",
        "Tunes",
        "Chaotic Tunes",
        "No Tunes",
        "doors",
        "dungeoncrawl",
        "Doors",
        "Dungeon Crawl",
        "doors_lite",
        "Doors Lite",
        "local",
    ]
    islocal = False
    if args:
        for x in args.split(" "):
            if x.strip().casefold() in local_args:
                islocal = True
                break
    flagstring = flags
    seed_desc = False
    dev = False
    mtype = "preset"
    steve_args = "STEVE "
    for x in args.split(" "):
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

        if x.strip() in ("fancygau", "Fancy Gau"):
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

        if x.strip() in ("nospoiler", "No Spoiler"):
            flagstring = flagstring.replace(" -sl ", " ")
            mtype += "_nospoiler"

        if x.strip() in ("noflashes", "No Flashes"):
            flagstring = "".join(
                [flagstring.replace(" -frm", "").replace(" -frw", ""), " -frw"]
            )
            mtype += "_noflashes"

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
                flagstring += " -dra"
                dev = "doors"
                mtype += "_doors"

        if x.strip() in ("dungeoncrawl", "Dungeon Crawl"):
            if dev == "dev":
                return await ctx.channel.send(
                    "Sorry, door rando doesn't work on dev currently"
                )
            else:
                flagstring += " -drdc"
                dev = "doors"
                mtype += "_dungeoncrawl"

        if x.strip() in ("doors_lite", "Doors Lite"):
            if dev == "dev":
                return await ctx.channel.send(
                    "Sorry, door rando doesn't work on dev currently"
                )
            else:
                flagstring += " -dre"
                dev = "doors"
                mtype += "_doors_lite"

        if "ap" in x.strip().casefold():
            try:
                ap_args = x.casefold().split("ap ")[1:][0].split()[0]
                if "gat" in ap_args:
                    ap_args = "on_with_additional_gating"
                elif ap_args == "on":
                    ap_args = "on"
                elif ap_args == "random":
                    ap_args = "random"
                else:
                    ap_args = "off"
            except IndexError:
                ap_args = "off"
            with open("db/template.yaml") as yaml:
                yaml_content = yaml.read()
            flagstring = (
                flagstring.replace("-open", "-cg")
                .replace("-lsced", "-lsc")
                .replace("-lsce ", "-lsc ")
                .replace("-hmced", "-hmc")
                .replace("-hmce ", "-hmc ")
            )
            with open("db/ap.yaml", "w", encoding="utf-8") as yaml_file:
                yaml_file.write(
                    yaml_content.replace("flags", flagstring)
                    .replace("ts_option", ap_args)
                    .replace(
                        "Player{number}",
                        "".join([ctx.author.display_name[:12], "_WC{NUMBER}"]),
                    )
                )
            return await ctx.channel.send(
                file=discord.File(
                    r"db/ap.yaml",
                    filename="".join(
                        [
                            ctx.author.display_name,
                            "_WC_",
                            mtype,
                            "_",
                            str(random.randint(0, 65535)),
                            ".yaml",
                        ]
                    ),
                )
            )

        if x.strip().casefold() == "flagsonly":
            return await ctx.channel.send(f"```{flagstring}```")

        if "steve" in x.strip().casefold():
            try:
                steve_args = x.split("steve ")[1:][0].split()[0]
                steve_args = "".join(ch for ch in steve_args if ch.isalnum())
            except IndexError:
                steve_args = "STEVE "

        if x.startswith("desc"):
            seed_desc = " ".join(x.split()[1:])
    return flagstring, mtype, islocal, seed_desc, steve_args, dev, local_args

async def parse_local_args(mtype, filename, steve_args, local_args, args):
    for x in args.split(" "):
            if x.strip().split(" ")[0] not in local_args:
                pass
            if "steve" in x.strip().casefold():
                bingo.steve.steveify(steve_args, filename)
                mtype += "_steve"
            if x.strip() == "True Loot":
                x = "true_loot"
            if x.strip().casefold() in (
                "loot",
                "true_loot",
                "all_pally",
                "top_tier",
                "poverty",
            ):
                bingo.randomize_drops.run_item_rando(local_args[x.strip().lower()])
                mtype += f"_{x.strip()}"
    for x in args.split(" "):
        if x.strip().casefold() == "tunes":
            await johnnydmad.johnnydmad("standard", filename)
            mtype += "_tunes"
            jdm_spoiler = True
        elif x.strip() in ("ctunes", "Chaotic Tunes"):
            if not jdm_spoiler:
                await johnnydmad.johnnydmad("chaos", filename)
                mtype += "_ctunes"
                jdm_spoiler = True
        elif x.strip() in ("notunes", "No Tunes"):
            if not jdm_spoiler:
                await johnnydmad.johnnydmad("silent", filename)
                mtype += "_notunes"
                jdm_spoiler = True


def purge_seed_files(f, d):
    filetypes = [".smc", ".zip", ".txt", "_spoiler.txt"]
    for x in filetypes:
        if os.path.isfile(d + f + x):
            os.remove(d + f + x)

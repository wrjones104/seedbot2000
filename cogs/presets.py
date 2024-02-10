import datetime
import functions
import sqlite3
import os
import json
import discord

from discord.ext import commands


class presets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="add", description="Add a new preset")
    async def add_preset(self, ctx, *args):
        pargs = await functions.preset_argparse(ctx.message.content)
        if pargs[5].casefold() == "true":
            user = await functions.get_user(ctx.message.author.id)
            try:
                if user and user[3] == 1:
                    official = True
                else:
                    return await ctx.channel.send(
                        "Only Racebot Admins can create official presets!"
                    )
            except AttributeError:
                return await ctx.channel.send(
                    "Presets cannot be set as `official` in DMs"
                )
        else:
            official = False
        if pargs[6].casefold() == "true":
            hidden = True
        else:
            hidden = False
        if "&" in pargs[0]:
            return await ctx.channel.send(
                "Presets don't support additional arguments. Save your preset with __FF6WC"
                " flags only__, then you can add arguments when you roll the preset with"
                " the **!preset <name>** command later."
            )
        if not pargs[1]:
            await ctx.channel.send(
                "Please provide a name for your preset with: **!add <name> --flags <flags> "
                "[--desc <optional description>]**"
            )
        else:
            if len(pargs[1]) > 64:
                return await ctx.channel.send(
                    "That name is too long! Make sure it's less than 64 characters!"
                )
            con = sqlite3.connect("db/seeDBot.sqlite")
            cur = con.cursor()
            cur.execute(
                "SELECT preset_name FROM presets WHERE preset_name = (?) COLLATE NOCASE",
                (pargs[2],),
            )
            if cur.fetchone():
                return await ctx.channel.send(
                    f"Preset name already exists! Try another name or use **!update_preset"
                    f" {pargs[1]} --flags <flags> [--desc <optional description>]** to overwrite"
                )
            else:
                cur.execute(
                    "INSERT INTO presets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        pargs[1],
                        ctx.author.id,
                        ctx.author.name,
                        datetime.datetime.utcnow(),
                        pargs[0],
                        pargs[3],
                        pargs[4].replace("&", ""),
                        official,
                        hidden,
                        False,
                    ),
                )
                con.commit()
                con.close()
                await ctx.channel.send(
                    f"Preset saved successfully! Use the command **!preset {pargs[1]}** to roll it!"
                )

            # TODO Remove all JSON sections when the website is ready
            # ------------------------------------------------------
            if not os.path.exists("db/user_presets.json"):
                with open("db/user_presets.json", "w") as newfile:
                    newfile.write(json.dumps({}))
            with open("db/user_presets.json") as preset_file:
                preset_dict = json.load(preset_file)
            if pargs[2] in preset_dict.keys():
                pass
            else:
                preset_dict[pargs[2]] = {
                    "name": pargs[1],
                    "creator_id": ctx.author.id,
                    "creator": ctx.author.name,
                    "flags": pargs[0],
                    "description": pargs[3],
                    "arguments": pargs[4].replace("&", ""),
                    "official": official,
                    "hidden": hidden,
                }
                with open("db/user_presets.json", "w") as updatefile:
                    updatefile.write(json.dumps(preset_dict))
            # ---------------------------------------------------------

    @commands.command(name="update")
    async def update_preset(self, ctx, *args):
        pargs = await functions.preset_argparse(ctx.message.content)
        flagstring = pargs[0]
        preset_name = pargs[1]
        preset_id = pargs[2]
        desc = pargs[3]
        preset_args = pargs[4]
        isofficial = pargs[5]
        ishidden = pargs[6]
        official = None
        hidden = None
        if isofficial:
            if isofficial.casefold() == "true":
                user = await functions.get_user(ctx.message.author.id)
                try:
                    if user and user[3] == 0:
                        return await ctx.channel.send(
                            "Only Racebot Admins can create official presets!"
                        )
                except AttributeError:
                    return await ctx.channel.send(
                        "Presets cannot be set as `official` in DMs"
                    )
                official = True
            elif isofficial.casefold() == "false":
                official = False
            else:
                official = None
        if ishidden:
            if ishidden.casefold() == "true":
                hidden = True
            elif ishidden.casefold() == "false":
                hidden = False
            else:
                hidden = None
        if "&" in flagstring:
            return await ctx.channel.send(
                "Presets don't support additional arguments. Save your preset with __FF6WC"
                " flags only__, then you can add arguments when you roll the preset with"
                " the **!preset <name>** command later."
            )
        if not preset_name:
            await ctx.channel.send(
                "Please provide a name for your preset with: **!update <name> --flags <flags> "
                "[--desc <optional description>]**"
            )
        else:
            con = sqlite3.connect("db/seeDBot.sqlite")
            cur = con.cursor()
            cur.execute(
                "SELECT preset_name, flags, description, arguments, official, hidden, creator_id FROM presets WHERE preset_name = (?) COLLATE NOCASE",
                (preset_id,),
            )
            thisquery = cur.fetchone()
            cur.execute(
                "SELECT preset_name FROM presets WHERE preset_name LIKE '%' || (?) || '%' AND creator_id = (?) COLLATE NOCASE ORDER BY gen_count DESC",
                (preset_id, ctx.author.id),
            )
            similar = cur.fetchmany(5)
            if not thisquery:
                sim = ""
                if similar:
                    sim = " Did you mean:```"
                    for x in similar:
                        sim += f"\n!update {x[0]}"
                    sim += "```"
                return await ctx.channel.send(
                    f"I couldn't find a preset with that name!{sim}"
                )
            else:
                if thisquery[6] != ctx.author.id:
                    return await ctx.channel.send(
                        "Sorry, you can't update a preset that you didn't create!"
                    )
                else:
                    if not flagstring:
                        flagstring = thisquery[1]
                    if not desc:
                        desc = thisquery[2]
                    if not preset_args:
                        preset_args = thisquery[3]
                    if official is None:
                        official = thisquery[4]
                    if hidden is None:
                        hidden = thisquery[5]
                    cur.execute(
                        "UPDATE presets SET flags = (?), description = (?), arguments = (?), official = (?), hidden = (?) WHERE preset_name = (?) COLLATE NOCASE",
                        (flagstring, desc, preset_args, official, hidden, preset_id),
                    )
                    con.commit()
                    con.close()
                    await ctx.channel.send("Preset updated successfully!")

            # TODO Remove all JSON sections when the website is ready
            # ------------------------------------------------------
            if not os.path.exists("db/user_presets.json"):
                with open("db/user_presets.json", "w") as newfile:
                    newfile.write(json.dumps({}))
            with open("db/user_presets.json") as preset_file:
                preset_dict = json.load(preset_file)
            if preset_id not in preset_dict.keys():
                pass
            elif preset_dict[preset_id]["creator_id"] == ctx.author.id:
                if not flagstring:
                    flagstring = preset_dict[preset_id]["flags"]
                if not flagstring:
                    flagstring = preset_dict[preset_id]["description"]
                if not preset_args:
                    try:
                        preset_args = preset_dict[preset_id]["arguments"]
                    except KeyError:
                        preset_dict[preset_id]["arguments"] = ""
                if official is None:
                    try:
                        official = preset_dict[preset_id]["official"]
                    except KeyError:
                        official = False
                if hidden is None:
                    try:
                        hidden = preset_dict[preset_id]["hidden"]
                    except KeyError:
                        hidden = False
                preset_dict[preset_id] = {
                    "name": preset_name,
                    "creator_id": ctx.author.id,
                    "creator": ctx.author.name,
                    "flags": flagstring,
                    "description": desc,
                    "arguments": preset_args.replace("&", ""),
                    "official": official,
                    "hidden": hidden,
                }
                with open("db/user_presets.json", "w") as updatefile:
                    updatefile.write(json.dumps(preset_dict))
            else:
                pass
            # ------------------------------------------------------

    @commands.command(name="delete")
    async def del_preset(self, ctx, *args):
        p_name = " ".join(ctx.message.content.split()[1:]).split("--flags")[0].strip()
        p_id = p_name.lower()
        if not p_name:
            await ctx.channel.send(
                "Please provide a name for the preset to delete with: **!delete <name>**"
            )
        else:
            con = sqlite3.connect("db/seeDBot.sqlite")
            cur = con.cursor()
            cur.execute(
                "SELECT preset_name, creator_id FROM presets WHERE preset_name = (?) COLLATE NOCASE",
                (p_id,),
            )
            thisquery = cur.fetchone()
            cur.execute(
                "SELECT preset_name FROM presets WHERE preset_name LIKE '%' || (?) || '%' AND creator_id = (?) COLLATE NOCASE ORDER BY gen_count DESC",
                (p_id, ctx.author.id),
            )
            similar = cur.fetchmany(5)
            if not thisquery:
                sim = ""
                if similar:
                    sim = " Did you mean:```"
                    for x in similar:
                        sim += f"\n!delete {x[0]}"
                    sim += "```"
                return await ctx.channel.send(
                    f"I couldn't find a preset with that name!{sim}"
                )
            else:
                if thisquery[1] != ctx.author.id:
                    return await ctx.channel.send(
                        "Sorry, you can't delete a preset that you didn't create!"
                    )
                else:
                    cur.execute(
                        "DELETE FROM presets WHERE preset_name = (?) COLLATE NOCASE",
                        (p_id,),
                    )
                    con.commit()
                    con.close()
                    await ctx.channel.send("Preset deleted successfully!")
            if not os.path.exists("db/user_presets.json"):
                with open("db/user_presets.json", "w") as newfile:
                    newfile.write(json.dumps({}))
            with open("db/user_presets.json") as preset_file:
                preset_dict = json.load(preset_file)
            if p_id not in preset_dict.keys():
                pass
            elif preset_dict[p_id]["creator_id"] == ctx.author.id:
                preset_dict.pop(p_id)
                with open("db/user_presets.json", "w") as updatefile:
                    updatefile.write(json.dumps(preset_dict))
            else:
                pass

    @commands.hybrid_command(
        name="mypresets",
        aliases=["my_presets"],
        description="Get a listing of all of your presets",
    )
    async def my_presets(self, ctx):
        con = sqlite3.connect("db/seeDBot.sqlite")
        cur = con.cursor()
        cur.execute(
            "SELECT preset_name, description, official FROM presets WHERE creator_id = (?)",
            (ctx.author.id,),
        )
        thisquery = cur.fetchall()
        if not thisquery:
            await ctx.send(
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
            await ctx.send("Here are all of the presets I have registered for you: \n")
            embed = discord.Embed()
            embed.title = f"{ctx.author.display_name}'s Presets"
            embed.description = plist
            try:
                await ctx.send(embed=embed)
            except Exception:
                with open("db/my_presets.txt", "w", encoding="utf-8") as preset_file:
                    preset_file.write(plist)
                return await ctx.send(file=discord.File(r"db/my_presets.txt"))

    @commands.hybrid_command(
        name="allpresets",
        aliases=["all_presets"],
        description="Get a file listing of all registered presets",
    )
    async def all_presets(self, ctx):
        con = sqlite3.connect("db/seeDBot.sqlite")
        cur = con.cursor()
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

        with open("db/all_presets.txt", "w", encoding="utf-8") as preset_file:
            preset_file.write(n_a_presets)
        return await ctx.send(
            f"Hey {ctx.author.display_name}," f" here are all saved presets:",
            file=discord.File(r"db/all_presets.txt"),
        )

    @commands.command(name="pflags", aliases=["p_flags", "presetflags", "preset_flags"])
    async def p_flags(self, ctx, *args):
        p_name = " ".join(ctx.message.content.split()[1:])
        p_id = p_name.lower()
        if not p_name:
            await ctx.channel.send("Please provide the name for the preset!")
        else:
            con = sqlite3.connect("db/seeDBot.sqlite")
            cur = con.cursor()
            cur.execute(
                "SELECT flags, hidden, preset_name FROM presets WHERE preset_name = (?) COLLATE NOCASE",
                (p_id,),
            )
            thisquery = cur.fetchone()
            simcur = con.cursor()
            simcur.execute(
                "SELECT preset_name FROM presets WHERE preset_name LIKE '%' || (?) || '%' COLLATE NOCASE ORDER BY gen_count DESC",
                (p_id,),
            )
            similar = simcur.fetchmany(5)
            if not thisquery:
                sim = ""
                if similar:
                    sim = " Did you mean:```"
                    for x in similar:
                        sim += f"\n!pflags {x[0]}"
                    sim += "```"
                return await ctx.channel.send(
                    f"I couldn't find a preset with that name!{sim}"
                )
            if thisquery[1]:
                return await ctx.channel.send(
                    "This is a hidden preset. If you are the author of this preset, check your DMs!"
                )
            else:
                return await ctx.channel.send(
                    f"The flags for **{thisquery[2]}** are:\n```{thisquery[0]}```"
                )


async def setup(bot):
    await bot.add_cog(presets(bot))

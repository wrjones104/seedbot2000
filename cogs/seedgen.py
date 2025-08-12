import functions
from core import flag_builder
import datetime
import components.views as views
import traceback
import os
import discord
from discord.ext import commands
from db.metric_writer import write_gsheets
from core.local_seed_generation import RollException
from core.seed_generator import argparse, generate_v1_seed, send_local_seed, purge_seed_files
from core.database import get_presets, increment_preset_count, save_buttons, update_seedlist
from core.seed_generator import splitargs


class seedgen(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="rollseed")
    async def rollseed(self, ctx, *args):
        msg = await ctx.send(f"Bundling up a seed for {ctx.author.display_name}...")
        flagstring = (
            " ".join(ctx.message.content.split("&")[:1])
            .replace("!rollseed", "")
            .strip()
        )
        try:
            argparse_result = await argparse(
                flagstring, await splitargs(args), "manually rolled"
            )
        except (RollException, ValueError) as e:
            await msg.edit(content=str(e))
            return
        except Exception:
            logid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            with open("db/error.txt", "w", encoding="utf-8") as error_file:
                error_file.write(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            await ctx.send(file=discord.File(r"db/error.txt"))
            return await msg.edit(content=f"There was an issue rolling this seed - see log")
        await rollchoice(ctx, argparse_result, msg, await splitargs(args), None)

    @commands.command(name="devseed")
    async def devseed(self, ctx, *args):
        msg = await ctx.send(f"Bundling up a seed for {ctx.author.display_name}...")
        flagstring = (
            " ".join(ctx.message.content.split("&")[:1]).replace("!devseed", "").strip()
        )
        try:
            argparse_result = await argparse(
                flagstring, await splitargs(args), "dev"
            )
        except (RollException, ValueError) as e:
            await msg.edit(content=str(e))
            return
        except Exception:
            logid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            with open("db/error.txt", "w", encoding="utf-8") as error_file:
                error_file.write(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            await ctx.send(file=discord.File(r"db/error.txt"))
            return await msg.edit(content=f"There was an issue rolling this seed - see log")
        await rollchoice(ctx, argparse_result, msg, await splitargs(args), None)

    @commands.command(name="rando")
    async def rando(self, ctx, *args):
        msg = await ctx.send(
            f"Bundling up a random seed for {ctx.author.display_name}..."
        )
        try:
            argparse_result = await argparse(
                await flag_builder.standard(),
                await splitargs(args),
                "standard",
            )
        except (RollException, ValueError) as e:
            await msg.edit(content=str(e))
            return
        except Exception:
            logid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            with open("db/error.txt", "w", encoding="utf-8") as error_file:
                error_file.write(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            await ctx.send(file=discord.File(r"db/error.txt"))
            return await msg.edit(content=f"There was an issue rolling this seed - see log")
        await rollchoice(ctx, argparse_result, msg, await splitargs(args), None)

    @commands.command(name="chaos")
    async def chaos(self, ctx, *args):
        msg = await ctx.send(f"Bundling up some chaos for {ctx.author.display_name}...")
        try:
            argparse_result = await argparse(
                await flag_builder.chaos(), await splitargs(args), "chaos"
            )
        except (RollException, ValueError) as e:
            await msg.edit(content=str(e))
            return
        except Exception:
            logid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            with open("db/error.txt", "w", encoding="utf-8") as error_file:
                error_file.write(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            await ctx.send(file=discord.File(r"db/error.txt"))
            return await msg.edit(content=f"There was an issue rolling this seed - see log")
        await rollchoice(ctx, argparse_result, msg, await splitargs(args), None)

    @commands.command(name="truechaos", aliases=["true", "true_chaos"])
    async def truechaos(self, ctx, *args):
        msg = await ctx.send(
            f"Bundling up **TRUE CHAOS** for {ctx.author.display_name}..."
        )
        try:
            argparse_result = await argparse(
                await flag_builder.true_chaos(),
                await splitargs(args),
                "truechaos",
            )
        except (RollException, ValueError) as e:
            await msg.edit(content=str(e))
            return
        except Exception:
            logid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            with open("db/error.txt", "w", encoding="utf-8") as error_file:
                error_file.write(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            await ctx.send(file=discord.File(r"db/error.txt"))
            return await msg.edit(content=f"There was an issue rolling this seed - see log")
        await rollchoice(ctx, argparse_result, msg, await splitargs(args), None)

    @commands.command(name="preset")
    async def preset(self, ctx, *args):
        msg = await ctx.send(f"Bundling up a preset for {ctx.author.display_name}...")
        if not " ".join(args).split("&")[0].strip():
            return await msg.edit(
                content="Please provide a preset name with your command, e.g.: `!preset ultros league`"
            )
        presets = await get_presets(" ".join(args).split("&")[0].strip())
        if presets[0]:
            preargs = presets[0][2].split()
            preargs = ["&" + word for word in preargs]
            args = args + tuple(preargs)
            try:
                argparse_result = await argparse(
                    presets[0][1],
                    await splitargs(args),
                    f"preset_{presets[0][0]}",
                )
            except (RollException, ValueError) as e:
                await msg.edit(content=str(e))
                return
            except Exception:
                logid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                with open("db/error.txt", "w", encoding="utf-8") as error_file:
                    error_file.write(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
                await ctx.send(file=discord.File(r"db/error.txt"))
                return await msg.edit(content=f"There was an issue rolling this seed - see log")
            await increment_preset_count(presets[0][0])
            await rollchoice(
                ctx, argparse_result, msg, await splitargs(args), presets[0]
            )
        else:
            args = " ".join(args).split("&")[1:]
            sim = None
            if presets[1]:
                viewid = datetime.datetime.now().strftime("%d%m%y%H%M%S%f")
                sim = " Did you mean:"
                viewids = []
                names = []
                ids = []
                flags = []
                bargs = []
                ispreset = []
                mtype = []
                for x in presets[1]:
                    viewids.append(viewid)
                    names.append(x[0])
                    ids.append(f"{viewid}_pcheck_{x[0]}")
                    flags.append(x[1])
                    preargs = x[2]
                    if args:
                        bargs.append("".join(preargs))
                    elif preargs:
                        bargs = "".join(preargs)
                    else:
                        bargs.append(False)
                    ispreset.append(True)
                    mtype.append(None)
                names_and_ids = list(
                    zip(viewids, names, ids, flags, bargs, ispreset, mtype)
                )
                await save_buttons(names_and_ids)
                view = views.ButtonView(names_and_ids)
                return await msg.edit(
                    content=f"That preset doesn't exist!{sim}", view=view
                )
            else:
                return await msg.edit(content="That preset doesn't exist!")

    @commands.command(name="practice")
    async def practice(self, ctx, *args):
        msg = await ctx.send(f"We talkin bout practice {ctx.author.display_name}...")
        try:
            argparse_result = await argparse(
                await flag_builder.practice(ctx.message.content),
                await splitargs(args),
                "practice",
            )
        except (RollException, ValueError) as e:
            await msg.edit(content=str(e))
            return
        except Exception:
            logid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            with open("db/error.txt", "w", encoding="utf-8") as error_file:
                error_file.write(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            await ctx.send(file=discord.File(r"db/error.txt"))
            return await msg.edit(content=f"There was an issue rolling this seed - see log")
        await rollchoice(ctx, argparse_result, msg, await splitargs(args), None)


async def roll_button_seed(
    ctx,
    button_name,
    button_id,
    button_flags,
    button_args,
    button_ispreset,
    button_mtype,
    msg,
    override,
):
    if button_args:
        bargs = list(button_args.split(" "))
    else:
        bargs = None
    if "Reroll with Extras" in button_id and not override:
        await msg.delete()
        await ctx.followup.send(
            "What do you want included in your reroll?",
            view=views.ReRollExtraView(
                ctx,
                button_name,
                button_id,
                button_flags,
                button_args,
                button_ispreset,
                "Reroll",
            ),
            ephemeral=True,
        )
    elif button_ispreset:
        await msg.edit(content=f"Rolling a seed for {ctx.user.display_name}...")
        presets = await get_presets(button_id.split("_")[2:][0])
        if presets[0]:
            try:
                argparse_result = await argparse(
                    presets[0][1], bargs, f"preset_{presets[0][0]}"
                )
            except (RollException, ValueError) as e:
                await msg.edit(content=str(e))
                return
            except Exception:
                logid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                with open("db/error.txt", "w", encoding="utf-8") as error_file:
                    error_file.write(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
                await ctx.send(file=discord.File(r"db/error.txt"))
                return await msg.edit(content=f"There was an issue rolling this seed - see log")
            await increment_preset_count(presets[0][0])
            await rollchoice(ctx, argparse_result, msg, button_args, presets[0])
        else:
            if button_args:
                args = " ".join(button_args).split("&")[1:]
            else:
                args = None
            sim = None
            if presets[1]:
                viewid = datetime.datetime.now().strftime("%d%m%y%H%M%S%f")
                sim = " Did you mean:"
                viewids = []
                names = []
                ids = []
                flags = []
                bargs = []
                ispreset = []
                for x in presets[1]:
                    viewids.append(viewid)
                    names.append(x[0])
                    ids.append(f"{viewid}_{x[0]}")
                    flags.append(x[1])
                    if args:
                        bargs.append("".join(args))
                    else:
                        bargs.append(False)
                    ispreset.append(True)
                names_and_ids = list(zip(viewids, names, ids, flags, bargs, ispreset))
                await save_buttons(names_and_ids)
                view = views.ButtonView(names_and_ids)
                return await msg.edit(
                    content=f"That preset doesn't exist!{sim}", view=view
                )
            else:
                return await msg.edit(content="That preset doesn't exist!")
    else:
        await msg.edit(content=f"Rerolling a seed for {ctx.user.display_name}...")
        for x in button_mtype:
            if x.split("_")[0] == "standard":
                flags = await flag_builder.standard()
            elif x.split("_")[0] == "chaos":
                flags = await flag_builder.chaos()
            elif x.split("_")[0] == "truechaos":
                flags = await flag_builder.true_chaos()
            else:
                flags = button_flags
        if button_mtype[:8] == "practice":
            bargs.append("practice")
        try:
            argparse_result = await argparse(flags, bargs, button_mtype)
        except (RollException, ValueError) as e:
            await msg.edit(content=str(e))
            return
        except Exception:
            logid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            with open("db/error.txt", "w", encoding="utf-8") as error_file:
                error_file.write(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            await ctx.send(file=discord.File(r"db/error.txt"))
            return await msg.edit(content=f"There was an issue rolling this seed - see log")
        await rollchoice(ctx, argparse_result, msg, button_args, None)


async def rollchoice(ctx, argparse_result, msg, args, preset=None):
    (
        flagstring,
        mtype,
        islocal,
        seed_desc,
        dev,
        filename,
        silly,
        jdm_spoiler,
        localhash,
    ) = argparse_result
    try:
        view = await functions.gen_reroll_buttons(
            ctx, preset, flagstring, args, mtype
        )
    except TypeError:
        return
    share_url = None
    if islocal:
        zip_path = await send_local_seed(filename, mtype, jdm_spoiler)
        if "preset" in mtype:
            await msg.edit(
                content=f"Here's your preset seed - {silly}\n**Preset Name**: {preset[0]}\n**Created By**:"
                f" {preset[3]}\n**Description**:"
                f" {preset[4]}\n**Hash**: {localhash}",
                attachments=[
                    discord.File(zip_path, filename=os.path.basename(zip_path))
                ],
                view=view,
            )
        else:
            await msg.edit(
                content=f"Here's your {mtype} seed - {silly}\n**Hash**: {localhash}",
                attachments=[
                    discord.File(zip_path, filename=os.path.basename(zip_path))
                ],
                view=view,
            )
        purge_seed_files(filename, "WorldsCollide/seeds/")
    else:
        try:
            share_url, seed_hash = await generate_v1_seed(flagstring, seed_desc, dev)
        except (RollException, KeyError, ValueError) as e:
            await msg.edit(content=str(e))
            return
        except Exception:
            logid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            with open("db/error.txt", "w", encoding="utf-8") as error_file:
                error_file.write(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            await ctx.send(file=discord.File(r"db/error.txt"))
            return await msg.edit(content=f"There was an issue rolling this seed - see log")

        if preset:
            await msg.edit(
                content=f"Here's your preset seed - {silly}\n"
                f"**Preset Name**: {preset[0]}\n"
                f"**Created By**: {preset[3]}\n"
                f"**Description**: {preset[4]}\n"
                f"**Hash**: {seed_hash}\n"
                f"> {share_url}",
                view=view,
            )
        else:
            await msg.edit(
                content=f"Here's your {mtype} seed - {silly}\n"
                f"**Hash**: {seed_hash}\n"
                f"> {share_url}",
                view=view,
            )
    if "paint" in mtype:
        p_type = True
    else:
        p_type = False
    try:
        server_name = ctx.guild.name
        server_id = ctx.guild.id
    except AttributeError:
        server_name = "DM"
        server_id = "N/A"
    try:
        channel_name = ctx.channel.name
        channel_id = ctx.channel.id
    except AttributeError:
        channel_name = "N/A"
        channel_id = "N/A"
    try:
        m = {
            "creator_id": ctx.author.id,
            "creator_name": ctx.author.name,
            "seed_type": mtype,
            "random_sprites": p_type,
            "share_url": share_url,
            "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")),
            "server_name": server_name,
            "server_id": server_id,
            "channel_name": channel_name,
            "channel_id": channel_id,
        }
    except (commands.errors.CommandInvokeError, AttributeError):
        m = {
            "creator_id": ctx.user.id,
            "creator_name": ctx.user.name,
            "seed_type": mtype,
            "random_sprites": p_type,
            "share_url": share_url,
            "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")),
            "server_name": server_name,
            "server_id": server_id,
            "channel_name": channel_name,
            "channel_id": channel_id,
        }
    except Exception as e:
        print(f"Couldn't bundle up seed information because of:\n{e}")
    await update_seedlist(m)
    try:
        await write_gsheets(m)
    except Exception as e:
        print(f'write_gsheets Exception: {e}')
        pass


async def setup(bot):
    await bot.add_cog(seedgen(bot))

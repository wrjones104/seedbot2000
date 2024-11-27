import functions
import flag_builder
import datetime
import components.views as views
import traceback
from discord.ext import commands
from db.metric_writer import write_gsheets


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
            argparse = await functions.argparse(
            ctx, flagstring, await functions.splitargs(args), "manually rolled"
        )
        except Exception:
            logid = functions.generate_file_name()
            print(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            return await msg.edit(content=f"There was an issue rolling this seed. - <@197757429948219392>, see log ID {logid}")
        await rollchoice(ctx, argparse, msg, await functions.splitargs(args), None)

    @commands.command(name="devseed")
    async def devseed(self, ctx, *args):
        msg = await ctx.send(f"Bundling up a seed for {ctx.author.display_name}...")
        flagstring = (
            " ".join(ctx.message.content.split("&")[:1]).replace("!devseed", "").strip()
        )
        try:
            argparse = await functions.argparse(
            ctx, flagstring, await functions.splitargs(args), "dev")
        except Exception:
            logid = functions.generate_file_name()
            print(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            return await msg.edit(content=f"There was an issue rolling this seed. - <@197757429948219392>, see log ID {logid}")
        await rollchoice(ctx, argparse, msg, await functions.splitargs(args), None)

    @commands.command(name="rando")
    async def rando(self, ctx, *args):
        msg = await ctx.send(
            f"Bundling up a random seed for {ctx.author.display_name}..."
        )
        try:
            argparse = await functions.argparse(
            ctx,
            await flag_builder.standard(),
            await functions.splitargs(args),
            "standard",
        )
        except Exception:
            logid = functions.generate_file_name()
            print(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            return await msg.edit(content=f"There was an issue rolling this seed. - <@197757429948219392>, see log ID {logid}")
        await rollchoice(ctx, argparse, msg, await functions.splitargs(args), None)

    @commands.command(name="chaos")
    async def chaos(self, ctx, *args):
        msg = await ctx.send(f"Bundling up some chaos for {ctx.author.display_name}...")
        try:
            argparse = await functions.argparse(
            ctx, await flag_builder.chaos(), await functions.splitargs(args), "chaos"
        )
        except Exception:
            logid = functions.generate_file_name()
            print(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            return await msg.edit(content=f"There was an issue rolling this seed. - <@197757429948219392>, see log ID {logid}")
        await rollchoice(ctx, argparse, msg, await functions.splitargs(args), None)

    @commands.command(name="truechaos", aliases=["true", "true_chaos"])
    async def truechaos(self, ctx, *args):
        msg = await ctx.send(
            f"Bundling up **TRUE CHAOS** for {ctx.author.display_name}..."
        )
        try:
            argparse = await functions.argparse(
            ctx, 
            await flag_builder.true_chaos(),
            await functions.splitargs(args),
            "truechaos",
        )
        except Exception:
            logid = functions.generate_file_name()
            print(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            return await msg.edit(content=f"There was an issue rolling this seed. - <@197757429948219392>, see log ID {logid}")
        await rollchoice(ctx, argparse, msg, await functions.splitargs(args), None)

    @commands.command(name="preset")
    async def preset(self, ctx, *args):
        msg = await ctx.send(f"Bundling up a preset for {ctx.author.display_name}...")
        if not " ".join(args).split("&")[0].strip():
            return await msg.edit(
                content="Please provide a preset name with your command, e.g.: `!preset ultros league`"
            )
        presets = await functions.get_presets(" ".join(args).split("&")[0].strip())
        if presets[0]:
            try:
                argparse = await functions.argparse(
                ctx, 
                presets[0][1],
                await functions.splitargs(args),
                f"preset_{presets[0][0]}",
            )
            except Exception:
                return await msg.edit(content=f"There was an issue with that flagset:```{presets[0][1]}```Please check the flags and try again.")
            await functions.increment_preset_count(presets[0][0])
            await rollchoice(
                ctx, argparse, msg, await functions.splitargs(args), presets[0]
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
                    if args:
                        bargs.append("".join(args))
                    else:
                        bargs.append(False)
                    ispreset.append(True)
                    mtype.append(None)
                names_and_ids = list(
                    zip(viewids, names, ids, flags, bargs, ispreset, mtype)
                )
                await functions.save_buttons(names_and_ids)
                view = views.ButtonView(names_and_ids)
                return await msg.edit(
                    content=f"That preset doesn't exist!{sim}", view=view
                )
            else:
                return await msg.edit(content="That preset doesn't exist!")
            
    # !practice command to roll a practice ROM seed
    @commands.command(name="practice")
    async def practice(self, ctx, *args):
        msg = await ctx.send(f"We talkin bout practice {ctx.author.display_name}...")
        # build the practice flagstring from the options given from the user, so pass in the message content
        # also we need to indicate to argparse that we're practice so it will run the seed generation with the right options
        try:
            argparse = await functions.argparse(
            ctx, await flag_builder.practice(ctx.message.content), await functions.splitargs(args), "practice"
        )
        except Exception:
            logid = functions.generate_file_name()
            print(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            return await msg.edit(content=f"There was an issue rolling this seed. - <@197757429948219392>, see log ID {logid}")
        await rollchoice(ctx, argparse, msg, await functions.splitargs(args), None)


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
        presets = await functions.get_presets(button_id.split("_")[2:][0])
        if presets[0]:
            try:
                argparse = await functions.argparse(
                ctx, presets[0][1], bargs, f"preset_{presets[0][0]}"
            )
            except Exception:
                logid = functions.generate_file_name()
                print(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
                return await msg.edit(content=f"There was an issue rolling this seed. - <@197757429948219392>, see log ID {logid}")
            await functions.increment_preset_count(presets[0][0])
            await rollchoice(ctx, argparse, msg, button_args, presets[0])
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
                await functions.save_buttons(names_and_ids)
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
                flags = flag_builder.standard()
            elif x.split("_")[0] == "chaos":
                flags = flag_builder.chaos()
            elif x.split("_")[0] == "truechaos":
                flags = flag_builder.true_chaos()
            else:
                flags = button_flags
        if button_mtype[:8] == "practice":
            bargs.append("practice")
        try:
            argparse = await functions.argparse(ctx, flags, bargs, button_mtype)
        except Exception:
            logid = functions.generate_file_name()
            print(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            return await msg.edit(content=f"There was an issue rolling this seed. - see logid {logid}")
        await rollchoice(ctx, argparse, msg, button_args, None)


async def rollchoice(ctx, argparse, msg, args, preset=None):
    view = await functions.gen_reroll_buttons(
        ctx, preset, argparse[0], args, argparse[1]
    )
    share_url = None
    if argparse[2]:
        await functions.send_local_seed(
            ctx, argparse[6], preset, argparse[5], argparse[7], argparse[1], msg, view, argparse[8]
        )
    else:
        try:
            share_url, seed_hash = await functions.generate_v1_seed(argparse[0], argparse[3], argparse[4])
        except KeyError:
            logid = functions.generate_file_name()
            print(f'--------------------\nlogid = {logid}\nctx content = {ctx.message.content}\n{traceback.format_exc()}--------------------')
            return await msg.edit(content=f"There was an error with this request - see log ID {logid}")
        if preset:
            await msg.edit(
                content=f"Here's your preset seed - {argparse[6]}\n"
                f"**Preset Name**: {preset[0]}\n"
                f"**Created By**: {preset[3]}\n"
                f"**Description**: {preset[4]}\n"
                f"**Hash**: {seed_hash}\n"
                f"> {share_url}",
                view=view,
            )
        else:
            await msg.edit(
                content=f"Here's your {argparse[1]} seed - {argparse[6]}\n"
                f"**Hash**: {seed_hash}\n"
                f"> {share_url}",
                view=view,
            )
    if "paint" in argparse[1].casefold():
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
            "seed_type": argparse[1],
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
            "seed_type": argparse[1],
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
    await functions.update_seedlist(m)
    try:
        await write_gsheets(m)
    except Exception as e:
        print(f'write_gsheets Exception: {e}')
        pass


async def setup(bot):
    await bot.add_cog(seedgen(bot))

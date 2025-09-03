import discord
import traceback
import datetime
from discord.ext import commands
from django.conf import settings
from webapp.models import Preset, SeedLog
from django.db.models import F
from asgiref.sync import sync_to_async

from bot import functions
from bot import flag_builder
from bot.components import views
from bot.utils.metric_writer import write_gsheets
from bot.utils.run_local import generate_local_seed, RollException
from bot.utils.tunes_processor import apply_tunes


class SeedGen(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(self, ctx: commands.Context, error: Exception):
        """Handles all errors for commands in this cog."""
        original_error = getattr(error, 'original', error)
        
        error_message = f"An unexpected error occurred. Please see error.txt for details."
        
        is_interaction = isinstance(ctx, discord.Interaction)
        
        error_details = f"Command: {ctx.command}\n"
        if hasattr(ctx, 'message'):
            error_details += f"Message: {ctx.message.content}\n"
        error_details += traceback.format_exc()

        if isinstance(original_error, RollException):
            error_message = f"There was an issue rolling this seed - see error.txt"
            error_details = (f"Command: {ctx.command}\n"
                             f"Message: {ctx.message.content if hasattr(ctx, 'message') else 'Interaction'}\n"
                             f"Filename: {original_error.filename}\nSubprocess Error:\n{original_error.sperror}\n"
                             f"--------------------\n{traceback.format_exc()}")
        
        error_log_path = settings.BASE_DIR / "data" / "error.txt"
        with open(error_log_path, "w", encoding="utf-8") as f:
            f.write(error_details)
        
        if is_interaction:
            if not ctx.response.is_done():
                await ctx.response.send_message(content=error_message, file=discord.File(error_log_path), ephemeral=True)
            else:
                await ctx.followup.send(content=error_message, file=discord.File(error_log_path), ephemeral=True)
        else:
            await ctx.send(content=error_message, file=discord.File(error_log_path))


    @commands.command(name="rollseed")
    async def rollseed(self, ctx, *args):
        msg = await ctx.send(f"Bundling up a seed for {ctx.author.display_name}...")
        flagstring = (
            " ".join(ctx.message.content.split("&")[:1])
            .replace("!rollseed", "")
            .strip()
        )
        options = await functions.argparse(ctx, flagstring, await functions.splitargs(args), "manually rolled")
        await _execute_roll(ctx, msg, options, args)

    @commands.command(name="devseed")
    async def devseed(self, ctx, *args):
        msg = await ctx.send(f"Bundling up a seed for {ctx.author.display_name}...")
        flagstring = " ".join(ctx.message.content.split("&")[:1]).replace("!devseed", "").strip()
        options = await functions.argparse(ctx, flagstring, await functions.splitargs(args), "dev")
        await _execute_roll(ctx, msg, options, args)

    @commands.command(name="rando")
    async def rando(self, ctx, *args):
        msg = await ctx.send(
            f"Bundling up a random seed for {ctx.author.display_name}..."
        )
        base_flags = await flag_builder.standard()
        options = await functions.argparse(ctx, base_flags, await functions.splitargs(args), "standard")
        await _execute_roll(ctx, msg, options, args)

    @commands.command(name="chaos")
    async def chaos(self, ctx, *args):
        msg = await ctx.send(f"Bundling up some chaos for {ctx.author.display_name}...")
        base_flags = await flag_builder.chaos()
        options = await functions.argparse(ctx, base_flags, await functions.splitargs(args), "chaos")
        print(f'chaos options: {options}')
        await _execute_roll(ctx, msg, options, args)

    @commands.command(name="truechaos", aliases=["true", "true_chaos"])
    async def truechaos(self, ctx, *args):
        msg = await ctx.send(
            f"Bundling up **TRUE CHAOS** for {ctx.author.display_name}..."
        )
        base_flags = await flag_builder.true_chaos()
        options = await functions.argparse(ctx, base_flags, await functions.splitargs(args), "truechaos")
        await _execute_roll(ctx, msg, options, args)

    @commands.command(name="preset")
    async def preset(self, ctx, *args):
        msg = await ctx.send(f"Bundling up a preset for {ctx.author.display_name}...")
        preset_name = " ".join(args).split("&")[0].strip()

        if not preset_name:
            return await msg.edit(content="Please provide a preset name!")

        try:
            preset_obj = await Preset.objects.aget(pk=preset_name)
            
            preargs = preset_obj.arguments.split() if preset_obj.arguments else []
            preargs = ["&" + word for word in preargs]
            final_args = args + tuple(preargs)
            
            options = await functions.argparse(
                ctx, preset_obj.flags, await functions.splitargs(final_args), f"preset_{preset_obj.preset_name}",
            )
            
            preset_obj.gen_count = F('gen_count') + 1
            await preset_obj.asave()
            
            await _execute_roll(ctx, msg, options, final_args, preset_obj)

        except Preset.DoesNotExist:
            return await msg.edit(content=f"That preset '{preset_name}' doesn't exist!")
            
    @commands.command(name="practice")
    async def practice(self, ctx, *args):
        msg = await ctx.send(f"We talkin bout practice {ctx.author.display_name}...")
        base_flags = await flag_builder.practice(ctx.message.content)
        options = await functions.argparse(ctx, base_flags, await functions.splitargs(args), "practice")
        await _execute_roll(ctx, msg, options, args)


async def _execute_roll(ctx, msg, options, args, preset_obj=None):
    if options.get("is_flagsonly"):
        await msg.edit(content=f"```{options['flagstring']}```")
        return

    if options.get("ap_option"):
        await _handle_ap_roll(ctx, msg, options)
        return

    share_url, seed_hash = None, None
    view = await functions.gen_reroll_buttons(ctx, preset_obj, options["flagstring"], args, options["mtype"])

    if options["is_local"]:
        seed_path, seed_id, seed_hash = generate_local_seed(
            flags=options["flagstring"],
            seed_type=options["dev_type"]
        )

        if options.get('tunes_type'):
            tunes_type = options['tunes_type']
            await msg.edit(content=f"Seed generated with `{options['dev_type'] or 'default'}` fork, now applying `{tunes_type}`...")
            apply_tunes(smc_path=seed_path, tunes_type=tunes_type)
        
        final_message = await functions.send_local_seed(
            ctx=ctx,
            silly=options["silly"],
            preset=preset_obj,
            mtype=options["mtype"],
            editmsg=msg,
            view=view,
            seed_hash=seed_hash,
            seed_path=seed_path,
            has_music_spoiler=options["jdm_spoiler"]
        )
        
        if final_message and final_message.attachments:
            share_url = final_message.attachments[0].url

    else:
        share_url, seed_hash = await functions.generate_v1_seed(
            options["flagstring"], options["seed_desc"], options["dev_type"]
        )
        
        content = f"Here's your {options['mtype']} seed - {options['silly']}\n**Hash**: {seed_hash}\n> {share_url}"
        if isinstance(preset_obj, Preset):
            content = (f"Here's your preset seed - {options['silly']}\n"
                       f"**Preset Name**: {preset_obj.preset_name}\n"
                       f"**Created By**: {preset_obj.creator_name}\n"
                       f"**Description**: {preset_obj.description}\n"
                       f"**Hash**: {seed_hash}\n"
                       f"> {share_url}")
        
        await msg.edit(content=content, view=view)
    
    await _log_seed_roll(ctx, options, args, share_url)


async def _log_seed_roll(ctx, options, args, share_url):
    """Gathers seed roll data and logs it to the database and Google Sheets."""
    p_type = "paint" in options["mtype"].casefold()
    author = getattr(ctx, 'author', getattr(ctx, 'user', None))

    print("\n" + "="*50)
    print(f"New Seed Rolled at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  - User: {author.name} ({author.id})")
    print(f"  - Type: {options['mtype']}")
    
    user_args = await functions.splitargs(args)
    if user_args:
        print(f"  - User Args: {', '.join(user_args)}")

    if options['is_local']:
        fork_used = options['dev_type'] or "Main WorldsCollide"
        print(f"  - Local Fork: {fork_used}")
    print("="*50 + "\n")

    try:
        server_name = ctx.guild.name if ctx.guild else "DM"
        server_id = ctx.guild.id if ctx.guild else "N/A"
        channel_name = ctx.channel.name if hasattr(ctx.channel, 'name') else "N/A"
        channel_id = ctx.channel.id if hasattr(ctx.channel, 'id') else "N/A"

        m = {
            "creator_id": author.id,
            "creator_name": author.name,
            "seed_type": options["mtype"],
            "random_sprites": p_type,
            "share_url": share_url,
            "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")),
            "server_name": server_name,
            "server_id": server_id,
            "channel_name": channel_name,
            "channel_id": channel_id,
        }
        
        # --- FIX: Use the standard Django ORM async method ---
        await SeedLog.objects.acreate(**m)
        write_gsheets(m)

    except Exception as e:
        print(f"Couldn't bundle up or log seed information because of:\n{e}")

async def handle_interaction_roll(interaction: discord.Interaction, button_info: tuple, extra_args: str = None):
    msg = await interaction.original_response()

    _, _, button_id, button_flags, button_args, is_preset, mtype = button_info
    
    final_args_list = button_args.split() if button_args else []
    if extra_args:
        final_args_list.extend(extra_args.split())
    final_args_tuple = tuple(final_args_list)

    preset_obj = None
    if is_preset:
        try:
            preset_name = button_id.split("_")[-1]
            preset_obj = await Preset.objects.aget(pk=preset_name)
            preset_obj.gen_count = F('gen_count') + 1
            await preset_obj.asave(update_fields=['gen_count'])
            
            button_flags = preset_obj.flags
            if preset_obj.arguments:
                final_args_list.extend(preset_obj.arguments.split())
                final_args_tuple = tuple(final_args_list)

        except Preset.DoesNotExist:
            return await interaction.followup.send(f"The preset '{preset_name}' seems to have been deleted.", ephemeral=True)

    options = await functions.argparse(interaction, button_flags, await functions.splitargs(final_args_tuple), mtype)
    
    await _execute_roll(interaction, msg, options, final_args_tuple, preset_obj)

async def _handle_ap_roll(ctx, msg, options):
    """A new helper function to generate and send the AP.yaml file."""
    await msg.edit(content="Generating Archipelago YAML file...")
    
    author = getattr(ctx, 'author', getattr(ctx, 'user', None))
    user_name = author.display_name
    ts_option = options["ap_option"]
    flagstring = options["flagstring"]
    
    template_path = settings.BASE_DIR / "data" / "template.yaml"
    with open(template_path, "r") as f:
        yaml_content = f.read()

    splitflags = [flag for flag in flagstring.split("-")]
    for i, flag in enumerate(splitflags):
        if flag.strip().startswith("name"):
            splitflags[i] = f'name {"".join(flag.split(" ")[1:]).replace(" ","")}'
        elif flag.strip().startswith("open"):
            splitflags[i] = 'cg '
    flagstring = "-".join(splitflags)

    ap_content = (
        yaml_content.replace("flags", flagstring.strip())
        .replace("ts_option", ts_option)
        .replace("Player{number}", f"{user_name[:12]}_WC{{NUMBER}}")
    )
    
    output_path = settings.BASE_DIR / "data" / "ap.yaml"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ap_content)
        
    discord_filename = f"{user_name}_{options['mtype']}_{options['filename']}.yaml"
    
    await ctx.channel.send(file=discord.File(output_path, filename=discord_filename))
    await msg.delete()

async def setup(bot):
    await bot.add_cog(SeedGen(bot))
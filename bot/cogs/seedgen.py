import discord
import traceback
import datetime
import asyncio
import functools
import logging
import tempfile
import shutil
import os
import difflib
from discord.ext import commands
from django.conf import settings
from webapp.models import Preset, SeedLog
from django.db.models import F
from pathlib import Path
from django.utils import timezone

from bot import functions
from bot import flag_builder
from bot.components import views
from bot.utils.metric_writer import write_gsheets
from bot.utils.run_local import generate_local_seed, RollException
from bot.utils.tunes_processor import apply_tunes
from bot.utils.steve_processor import steveify

logger = logging.getLogger(__name__)


class SeedGen(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(self, ctx: commands.Context, error: Exception):
        """Handles all errors for commands in this cog."""
        original_error = getattr(error, 'original', error)

        if isinstance(original_error, discord.errors.NotFound) and original_error.code == 10062:
            print(f"Ignoring error handler for an unknown interaction (ID: {ctx.id}). It likely expired or is from before a restart.")
            return
        
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
        
        tmp_file = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tmp_file:
                tmp_file.write(error_details)
                error_log_path = tmp_file.name

            if is_interaction:
                if ctx.response.is_done():
                    await ctx.followup.send(content=error_message, file=discord.File(error_log_path), ephemeral=True)
                else:
                    await ctx.response.send_message(content=error_message, file=discord.File(error_log_path), ephemeral=True)
            else:
                await ctx.send(content=error_message, file=discord.File(error_log_path))
        finally:
            if tmp_file:
                os.remove(tmp_file.name)


    @commands.command(name="rollseed")
    async def rollseed(self, ctx, *args):
        """
        Rolls a seed with a given flagstring. Addon arguments can be supplied, prefixed with '&'.
        Example: !rollseed -flags... &tunes &paint
        """
        msg = await ctx.send(f"Bundling up a seed for {ctx.author.display_name}...")
        full_args_string = ctx.message.content[len(f"{ctx.prefix}{ctx.invoked_with}"):].strip()
        parts = full_args_string.split('&')
        flagstring = parts[0].strip()
        addon_args = tuple(part.strip() for part in parts[1:] if part.strip())
        options = await functions.argparse(ctx, flagstring, await functions.splitargs(addon_args), "manually rolled")
        await _execute_roll(ctx, msg, options, addon_args)

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
        base_flags = flag_builder.standard()
        options = await functions.argparse(ctx, base_flags, await functions.splitargs(args), "standard")
        await _execute_roll(ctx, msg, options, args)

    @commands.command(name="chaos")
    async def chaos(self, ctx, *args):
        msg = await ctx.send(f"Bundling up some chaos for {ctx.author.display_name}...")
        base_flags = flag_builder.chaos()
        options = await functions.argparse(ctx, base_flags, await functions.splitargs(args), "chaos")
        await _execute_roll(ctx, msg, options, args)

    @commands.command(name="truechaos", aliases=["true", "true_chaos"])
    async def truechaos(self, ctx, *args):
        msg = await ctx.send(
            f"Bundling up **TRUE CHAOS** for {ctx.author.display_name}..."
        )
        base_flags = flag_builder.true_chaos()
        options = await functions.argparse(ctx, base_flags, await functions.splitargs(args), "truechaos")
        await _execute_roll(ctx, msg, options, args)

    @commands.command(name="preset")
    async def preset(self, ctx, *args):
        msg = await ctx.send(f"Bundling up a preset for {ctx.author.display_name}...")
        
        if not args:
            return await msg.edit(content="Please provide a preset name!")

        full_input_str = " ".join(args)
        parts = full_input_str.split('&', 1)
        preset_name = parts[0].strip()

        extra_args_tuple = tuple(f"&{parts[1]}".split()) if len(parts) > 1 else tuple()

        try:
            preset_obj = await Preset.objects.aget(preset_name__iexact=preset_name)
            
            preset_args = preset_obj.arguments.split() if preset_obj.arguments else []
            extra_args_list = await functions.splitargs(extra_args_tuple) if extra_args_tuple else []
            final_args_list = preset_args + extra_args_list
            
            options = await functions.argparse(
                ctx,
                preset_obj.flags,
                final_args_list,
                f"preset_{preset_obj.preset_name.replace(' ', '_')}"
            )
            
            preset_obj.gen_count = F('gen_count') + 1
            await preset_obj.asave(update_fields=['gen_count'])
            
            await _execute_roll(ctx, msg, options, tuple(final_args_list), preset_obj)

        except Preset.DoesNotExist:
            all_preset_names = [p['preset_name'] async for p in Preset.objects.values('preset_name')]
            similar_matches = difflib.get_close_matches(preset_name, all_preset_names, n=5, cutoff=0.6)
            
            if similar_matches:
                embed = discord.Embed(
                    title="🤔 Preset Not Found",
                    description=f"I couldn't find a preset named '{preset_name}'. Did you mean one of these?",
                    color=discord.Color.gold()
                )
                
                matched_presets = [p async for p in Preset.objects.filter(preset_name__in=similar_matches)]
                
                suggestions_text = [f"**{p.preset_name}** (by {p.creator_name})" for p in matched_presets]
                embed.add_field(name="Suggestions", value="\n".join(suggestions_text), inline=False)

                extra_args_list = await functions.splitargs(extra_args_tuple)
                original_args_str = " ".join(extra_args_list)

                view = views.PresetSuggestionView(suggestions=matched_presets, original_args_str=original_args_str)
                
                edited_msg = await msg.edit(content="", embed=embed, view=view)
                view.message = edited_msg
            else:
                await msg.edit(content=f"I couldn't find a preset named '{preset_name}'!")
            
    @commands.command(name="practice")
    async def practice(self, ctx, *args):
        msg = await ctx.send(f"We talkin bout practice {ctx.author.display_name}...")
        base_flags = flag_builder.practice(ctx.message.content)
        options = await functions.argparse(ctx, base_flags, await functions.splitargs(args), "practice")
        await _execute_roll(ctx, msg, options, args)


async def _execute_roll(ctx, msg, options, args, preset_obj=None):
    user = getattr(ctx, 'author', getattr(ctx, 'user', None))
    logger.debug(f"Initiating _execute_roll for user {user.name} ({user.id})")
    logger.debug(f"Mtype: {options.get('mtype')}, Is Local: {options.get('is_local')}")
    logger.debug(f"Preset supplied: {preset_obj.preset_name if preset_obj else 'None'}")
    logger.debug(f"Flagstring: {options.get('flagstring')}")
    is_interaction = isinstance(ctx, discord.Interaction)

    if options.get("is_flagsonly"):
        if is_interaction:
            await ctx.followup.send(f"```{options['flagstring']}```", ephemeral=True)
        else:
            await msg.edit(content=f"```{options['flagstring']}```")
        return

    if options.get("ap_option"):
        logger.debug("Executing local roll.")
        await _handle_ap_roll(ctx, msg, options)
        return

    seed_log = await _log_seed_roll(ctx, options, args)
    if not seed_log:
        error_msg = "Failed to log seed information before rolling. Aborting."
        if is_interaction:
            # Use followup for deferred interactions, response for new ones
            if ctx.response.is_done():
                await ctx.followup.send(error_msg, ephemeral=True)
            else:
                await ctx.response.send_message(error_msg, ephemeral=True)
        else:
            await msg.edit(content=error_msg)
        return

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Reroll", style=discord.ButtonStyle.primary, custom_id=f"persistent_reroll:{seed_log.id}"))
    view.add_item(discord.ui.Button(label="Reroll with Extras", style=discord.ButtonStyle.secondary, custom_id=f"persistent_extras:{seed_log.id}"))

    share_url, seed_hash = None, None

    if options["is_local"]:
        temp_dir = Path(tempfile.mkdtemp())
        try:
            loop = asyncio.get_running_loop()
            blocking_task = functools.partial(
                generate_local_seed,
                flags=options["flagstring"],
                seed_type=options["dev_type"],
                output_dir=temp_dir
            )
            seed_path, seed_id, seed_hash = await loop.run_in_executor(
                None, blocking_task
            )
            logger.debug(f"Local seed generated: ID {seed_id}, Path {seed_path}")

            if options.get('tunes_type'):
                tunes_type = options['tunes_type']
                logger.debug(f"Applying tunes: {tunes_type} to seed ID {seed_id}")
                status_update = f"Seed generated with `{options['dev_type'] or 'default'}` fork, now applying `{tunes_type}`..."
                if is_interaction:
                    await ctx.followup.send(status_update, ephemeral=True)
                else:
                    await msg.edit(content=status_update)

                with open(seed_path, 'rb') as f:
                    in_rom_bytes = f.read()

                tuned_rom_bytes, music_spoiler_content = apply_tunes(in_rom_bytes, tunes_type=tunes_type)

                with open(seed_path, 'wb') as f:
                    f.write(tuned_rom_bytes)
                
                spoiler_path = seed_path.with_suffix('.txt').with_stem(f"{seed_path.stem}_music_spoiler")
                with open(spoiler_path, 'w', encoding='utf-8') as f:
                    f.write(music_spoiler_content)

            if options.get('steve_name'):
                steve_name = options['steve_name']
                logger.debug(f"Steve-ifying seed with name '{steve_name}'")
                status_update = f"Seed customization complete, now applying `{steve_name}`..."
                if is_interaction:
                    await ctx.followup.send(status_update, ephemeral=True)
                else:
                    await msg.edit(content=status_update)
                steveify(s=steve_name, smc_path=seed_path)
            
            content, zip_path = await functions.send_local_seed(
                silly=options["silly"],
                preset=preset_obj,
                mtype=options["mtype"],
                seed_hash=seed_hash,
                seed_path=seed_path,
                has_music_spoiler=options["jdm_spoiler"]
            )

            final_message = None
            if zip_path:
                discord_file = discord.File(zip_path)
                if is_interaction:
                    final_message = await ctx.followup.send(content, file=discord_file, view=view)
                else:
                    await msg.delete()
                    final_message = await ctx.send(content, file=discord_file, view=view)
                os.remove(zip_path)
            else:
                if is_interaction:
                    await ctx.followup.send(content, ephemeral=True)
                else:
                    await msg.edit(content=content)
            
            if final_message and final_message.attachments:
                share_url = final_message.attachments[0].url

        finally:
            shutil.rmtree(temp_dir)
            logger.debug(f"Cleaned up temporary directory {temp_dir}")

    else:
        logger.debug("Executing web API roll.")
        share_url, seed_hash = await functions.generate_v1_seed(
            options["flagstring"], options["seed_desc"], options["dev_type"]
        )
        logger.debug(f"Web API seed generated: Hash {seed_hash}, Share URL {share_url}")
        
        content = f"Here's your {options['mtype']} seed - {options['silly']}\n**Hash**: {seed_hash}\n> {share_url}"
        if isinstance(preset_obj, Preset):
            content = (f"Here's your preset seed - {options['silly']}\n"
                       f"**Preset Name**: {preset_obj.preset_name}\n"
                       f"**Created By**: {preset_obj.creator_name}\n"
                       f"**Description**: {preset_obj.description}\n"
                       f"**Hash**: {seed_hash}\n"
                       f"> {share_url}")
        
        if is_interaction:
            await ctx.followup.send(content, view=view)
        else:
            await msg.edit(content=content, view=view)
    
    if share_url:
        seed_log.share_url = share_url
        await seed_log.asave(update_fields=['share_url'])


async def _log_seed_roll(ctx, options, args):
    """Gathers seed roll data and logs it to the database and Google Sheets."""
    author = getattr(ctx, 'author', getattr(ctx, 'user', None))
    
    try:
        server_name = ctx.guild.name if ctx.guild else "DM"
        server_id = ctx.guild.id if ctx.guild else None
        channel_name = ctx.channel.name if hasattr(ctx.channel, 'name') else "N/A"
        channel_id = ctx.channel.id if hasattr(ctx.channel, 'id') else None

        m = {
            "creator_id": author.id,
            "creator_name": author.name,
            "seed_type": options["mtype"],
            "random_sprites": "paint" in options["mtype"].casefold(),
            "timestamp": timezone.now(),
            "server_name": server_name,
            "server_id": server_id,
            "channel_name": channel_name,
            "channel_id": channel_id,
            "share_url": None,
            "flagstring": options["flagstring"],
            "args_list": list(args) if args else [],
        }
        
        # Create the object and get it back
        seed_log_obj = await SeedLog.objects.acreate(**m)
        
        # Log to Google Sheets
        write_gsheets(m)

        # Return the new database object
        return seed_log_obj

    except Exception as e:
        print(f"Couldn't bundle up or log seed information because of:\n{e}")
        return None

async def handle_interaction_roll(interaction: discord.Interaction, button_info: tuple, final_args_str: str = None):
    """
    Handles a roll from a button click. If final_args_str is provided, it comes
    from the RerollModal and overrides any previous arguments.
    """
    _, _, button_id, base_flags, original_args_str, is_preset_int, original_mtype = button_info
    is_preset = bool(is_preset_int)

    args_to_use = final_args_str if final_args_str is not None else original_args_str
    final_args_tuple = tuple(args_to_use.split()) if args_to_use else tuple()

    preset_obj = None
    base_mtype = original_mtype
    
    if is_preset:
        try:
            temp_id = original_mtype.replace("preset_", "", 1)
            
            args_slug = ""
            if original_args_str:
                args_slug = "_" + "_".join(original_args_str.lower().split())
            
            preset_slug = temp_id
            if args_slug and temp_id.endswith(args_slug):
                preset_slug = temp_id[:-len(args_slug)]

            identifier = preset_slug.replace("_", " ")

            preset_obj = await Preset.objects.aget(preset_name__iexact=identifier)
            base_flags = preset_obj.flags
            base_mtype = f"preset_{preset_obj.preset_name.replace(' ', '_')}"
            
            if final_args_str is None and preset_obj.arguments:
                combined_args = set(final_args_tuple + tuple(preset_obj.arguments.split()))
                final_args_tuple = tuple(combined_args)

        except Preset.DoesNotExist:
            return await interaction.followup.send(f"The preset '{identifier}' seems to have been deleted.", ephemeral=True)
    else:
        # For non-presets, extract the base type (e.g., 'standard' from 'standard_tunes')
        base_mtype = original_mtype.split('_')[0]

    options = await functions.argparse(
        interaction, 
        base_flags, 
        final_args_tuple, 
        base_mtype
    )
    
    if preset_obj:
        preset_obj.gen_count = F('gen_count') + 1
        await preset_obj.asave(update_fields=['gen_count'])
    
    await _execute_roll(interaction, None, options, final_args_tuple, preset_obj)


async def _handle_ap_roll(ctx, msg, options):
    """A new helper function to generate and send the AP.yaml file."""
    is_interaction = isinstance(ctx, discord.Interaction)
    if is_interaction:
        await ctx.followup.send("Generating Archipelago YAML file...", ephemeral=True)
    else:
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
            splitflags[i] = f'name {"".join(flag.split(" ")[1:]).replace(" ","")} '
        elif flag.strip().startswith("open"):
            splitflags[i] = 'cg '
    flagstring = "-".join(splitflags)

    ap_content = (
        yaml_content.replace("flags", flagstring.strip())
        .replace("ts_option", ts_option)
        .replace("Player{number}", f"{user_name[:12]}_WC{{NUMBER}}")
    )
    
    tmp_file = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yaml', encoding='utf-8') as tmp_file:
            tmp_file.write(ap_content)
            output_path = tmp_file.name
            
        discord_filename = f"{user_name}_{options['mtype']}_{options['filename']}.yaml"    
        await ctx.channel.send(file=discord.File(output_path, filename=discord_filename))
        
        if not is_interaction:
            await msg.delete()
    finally:
        if tmp_file:
            os.remove(tmp_file.name)

async def setup(bot):
    await bot.add_cog(SeedGen(bot))

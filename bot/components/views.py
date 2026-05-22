import discord
from discord.ui import View, Modal, TextInput
from discord.ext import commands
from typing import cast, Optional
from webapp.models import Preset, SeedLog

from bot.constants import SHORT_TIMEOUT


class RerollModal(Modal):
    """
    A modal popup that allows users to edit arguments before rerolling.
    This is now invoked by the persistent view.
    """
    def __init__(self, seed_log: SeedLog):
        super().__init__(title="Customize Your Reroll")
        self.seed_log = seed_log
        self.original_args_str = " ".join(seed_log.args_list or [])

        self.arguments_input = TextInput(
            label="Arguments",
            style=discord.TextStyle.paragraph,
            placeholder="Enter arguments separated by spaces (e.g., tunes paint kupo)",
            default=self.original_args_str,
            required=False,
        )
        self.add_item(self.arguments_input)

    async def on_submit(self, interaction: discord.Interaction):
        from bot.cogs.seedgen import handle_interaction_roll

        await interaction.response.defer(thinking=True, ephemeral=True)
        final_arguments_str = self.arguments_input.value
        
        button_info = (
            None, 
            "Reroll with Extras",
            None, 
            self.seed_log.flagstring,
            self.original_args_str,
            "preset" in self.seed_log.seed_type, # is_preset check
            self.seed_log.seed_type
        )
        await handle_interaction_roll(interaction, button_info, final_args_str=final_arguments_str)


async def _get_seed_log(interaction: discord.Interaction) -> Optional[SeedLog]:
    """Helper to parse ID from custom_id and fetch the SeedLog object."""
    try:
        seed_log_id = int(interaction.data['custom_id'].split(':')[1])
        return await SeedLog.objects.aget(pk=seed_log_id)
    except (IndexError, ValueError, SeedLog.DoesNotExist):
        await interaction.response.send_message(
            "I can't find the data for this seed. It might be from a very old roll.", 
            ephemeral=True
        )
        return None

async def _handle_view_error(interaction: discord.Interaction, error: Exception):
    """Centralized error handling for view functions."""
    from bot.cogs.seedgen import SeedGen # Local import
    bot = cast(commands.Bot, interaction.client)
    cog: SeedGen = bot.get_cog('SeedGen')
    if cog:
        await cog.cog_command_error(interaction, error)
    else:
        if not interaction.response.is_done():
            await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)
        else:
            await interaction.followup.send("An unexpected error occurred.", ephemeral=True)

async def handle_reroll_button_click(interaction: discord.Interaction):
    """Handles the logic for the simple 'Reroll' button."""
    from bot.cogs.seedgen import handle_interaction_roll # Local import
    try:
        await interaction.response.defer(thinking=True, ephemeral=True)
        seed_log = await _get_seed_log(interaction)
        if not seed_log:
            return

        original_args_str = " ".join(seed_log.args_list or [])
        button_info = (
            None, "Reroll", None,
            seed_log.flagstring,
            original_args_str,
            "preset" in seed_log.seed_type,
            seed_log.seed_type
        )
        await handle_interaction_roll(interaction, button_info)
    except Exception as e:
        await _handle_view_error(interaction, e)

async def handle_extras_button_click(interaction: discord.Interaction):
    """Handles the logic for the 'Reroll with Extras' button."""
    try:
        seed_log = await _get_seed_log(interaction)
        if not seed_log:
            if not interaction.response.is_done():
                await interaction.response.send_message("Could not find seed data.", ephemeral=True)
            return

        modal = RerollModal(seed_log=seed_log)
        await interaction.response.send_modal(modal)
    except Exception as e:
        await _handle_view_error(interaction, e)

class RollSuggestionButton(discord.ui.Button):
    """A button that, when clicked, rolls a specific preset suggestion."""
    def __init__(self, preset: Preset, original_args_str: str):
        super().__init__(style=discord.ButtonStyle.primary, label=preset.preset_name)
        self.preset = preset
        self.original_args_str = original_args_str

    async def callback(self, interaction: discord.Interaction):
        # Local import to avoid circular dependency
        from bot.cogs.seedgen import handle_interaction_roll

        self.view.stop()
        for item in self.view.children:
            item.disabled = True
        await interaction.response.edit_message(content=f"✅ Rolling `{self.preset.preset_name}` for you...", view=self.view)

        button_info = (
            None, "Roll", f"suggestion_roll_{self.preset.pk}",
            self.preset.flags, self.original_args_str, 1,
            f"preset_{self.preset.preset_name.replace(' ', '_')}"
        )
        await handle_interaction_roll(interaction, button_info)

class PresetSuggestionView(discord.ui.View):
    """A view that displays multiple RollSuggestionButtons."""
    def __init__(self, *, suggestions: list[Preset], original_args_str: str, timeout=180):
        super().__init__(timeout=timeout)
        self.message: discord.Message = None

        for preset in suggestions:
            self.add_item(RollSuggestionButton(preset, original_args_str))
            
    async def on_timeout(self):
        if self.message:
            for item in self.children:
                item.disabled = True
            await self.message.edit(content="Suggestion buttons timed out.", view=self)
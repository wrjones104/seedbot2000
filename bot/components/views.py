import discord
from discord.ui import View, Modal, TextInput
from discord.ext import commands
from typing import cast, List, Optional
from webapp.models import Preset

from bot.constants import DEFAULT_TIMEOUT
from bot.cogs.seedgen import handle_interaction_roll, SeedGen


class RerollModal(Modal):
    """A modal popup that allows users to edit arguments before rerolling."""
    def __init__(self, flags: str, original_args: str, mtype: str):
        super().__init__(title="Customize Your Reroll")
        self.flags = flags
        self.original_args = original_args
        self.mtype = mtype

        self.arguments_input = TextInput(
            label="Arguments",
            style=discord.TextStyle.paragraph,
            placeholder="Enter arguments separated by spaces (e.g., tunes paint kupo)",
            default=self.original_args,
            required=False,
        )
        self.add_item(self.arguments_input)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=True)
        final_arguments_str = self.arguments_input.value
        
        button_info = (
            None, 
            "Reroll with Extras",
            None, 
            self.flags,
            self.original_args,
            "preset" in self.mtype, # is_preset check
            self.mtype
        )
        await handle_interaction_roll(interaction, button_info, final_args_str=final_arguments_str)


class RerollView(View):
    """
    A view containing 'Reroll' and 'Reroll with Extras' buttons.
    This view holds its own state and does not require database persistence.
    """
    def __init__(self, flags: str, args: Optional[List[str]], mtype: str):
        super().__init__(timeout=DEFAULT_TIMEOUT)
        self.flags = flags
        self.args_list = args if args else []
        self.args_str = " ".join(self.args_list)
        self.mtype = mtype
        self.message: Optional[discord.Message] = None
        
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=self)

    @discord.ui.button(label="Reroll", style=discord.ButtonStyle.primary)
    async def reroll_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.defer(thinking=True, ephemeral=True)
            
            button_info = (
                None,
                "Reroll",
                None,
                self.flags,
                self.args_str,
                "preset" in self.mtype,
                self.mtype
            )
            await handle_interaction_roll(interaction, button_info)
        except Exception as e:
            await self._handle_error(interaction, e)

    @discord.ui.button(label="Reroll with Extras", style=discord.ButtonStyle.secondary)
    async def extras_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            modal = RerollModal(
                flags=self.flags,
                original_args=self.args_str,
                mtype=self.mtype
            )
            await interaction.response.send_modal(modal)
        except Exception as e:
            await self._handle_error(interaction, e)
            
    async def _handle_error(self, interaction: discord.Interaction, error: Exception):
        """Centralized error handling for the view."""
        bot = cast(commands.Bot, interaction.client)
        cog: SeedGen = bot.get_cog('SeedGen')
        if cog:
            await cog.cog_command_error(interaction, error)
        else:
            # Fallback error message
            if not interaction.response.is_done():
                await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)
            else:
                await interaction.followup.send("An unexpected error occurred.", ephemeral=True)

class RollSuggestionButton(discord.ui.Button):
    """A button that, when clicked, rolls a specific preset suggestion."""
    def __init__(self, preset: Preset, original_args_str: str):
        super().__init__(style=discord.ButtonStyle.primary, label=preset.preset_name)
        self.preset = preset
        self.original_args_str = original_args_str

    async def callback(self, interaction: discord.Interaction):
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
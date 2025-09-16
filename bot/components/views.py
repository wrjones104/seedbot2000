import discord
from discord.ui import View, Modal, TextInput
from discord.ext import commands
from typing import cast, List, Optional

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
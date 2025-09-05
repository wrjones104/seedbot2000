import discord
from discord.ui import View, Modal, TextInput
from discord.ext import commands
from typing import cast

from bot.functions import get_button_info
from bot.cogs.seedgen import handle_interaction_roll, SeedGen


class RerollModal(Modal):
    """A modal popup that allows users to edit arguments before rerolling."""
    def __init__(self, button_info: tuple):
        super().__init__(title="Customize Your Reroll")
        self.button_info = button_info
        
        # Unpack the original arguments to pre-fill the text box
        _, _, _, _, original_args, _, _ = self.button_info
        
        self.arguments_input = TextInput(
            label="Arguments",
            style=discord.TextStyle.paragraph,
            placeholder="Enter arguments separated by spaces (e.g., tunes paint kupo)",
            default=original_args,
            required=False,
        )
        self.add_item(self.arguments_input)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=True)
        final_arguments_str = self.arguments_input.value
        await handle_interaction_roll(interaction, self.button_info, final_args_str=final_arguments_str)


class RerollExtrasButton(discord.ui.Button):
    """A dedicated button that opens the RerollModal."""
    def __init__(self, original_args: str, **kwargs):
        super().__init__(**kwargs)
        self.original_args = original_args

    async def callback(self, interaction: discord.Interaction):
        try:
            button_info = await get_button_info(self.custom_id)
            
            # --- FIX: Add a safety check for missing button data ---
            if not button_info:
                await interaction.response.send_message(
                    "Sorry, the data for this button has expired. Please roll a new seed.", 
                    ephemeral=True
                )
                return
            
            modal = RerollModal(button_info=button_info)
            await interaction.response.send_modal(modal)
        except Exception as e:
            bot = cast(commands.Bot, interaction.client)
            cog: SeedGen = bot.get_cog('SeedGen')
            if cog:
                await cog.cog_command_error(interaction, e)


class PersistentButton(discord.ui.Button):
    """A button that immediately triggers a reroll."""
    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(thinking=True, ephemeral=True)
            button_info = await get_button_info(self.custom_id)

            # --- FIX: Add a safety check for missing button data ---
            if not button_info:
                await interaction.followup.send(
                    "Sorry, the data for this button has expired. Please roll a new seed.",
                    ephemeral=True
                )
                return

            await handle_interaction_roll(interaction, button_info)
        except Exception as e:
            bot = cast(commands.Bot, interaction.client)
            cog: SeedGen = bot.get_cog('SeedGen')
            if cog:
                await cog.cog_command_error(interaction, e)
            else:
                # Fallback error message
                if interaction.response.is_done():
                    await interaction.followup.send("An unexpected error occurred.", ephemeral=True)


class ButtonView(discord.ui.View):
    def __init__(self, options_and_ids):
        super().__init__(timeout=None)
        for data_tuple in options_and_ids:
            _, option, button_id, _, _, _, _ = data_tuple
            button = PersistentButton(
                label=option, custom_id=button_id, style=discord.ButtonStyle.green
            )
            self.add_item(button)
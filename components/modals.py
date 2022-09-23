import discord
from discord.ui import Modal, TextInput, Select
from discord import TextStyle, Interaction


class NewPresetModal(Modal):
    preset_name = TextInput(
        label="Preset Name",
        style=TextStyle.short,
    )

    preset_flags = TextInput(
        label="Enter the flags for the preset",
        style=TextStyle.long,
    )

    preset_desc = TextInput(
        label="Enter a description for the preset",
        style=TextStyle.long,
    )

    def __init__(self, title: str) -> None:
        super().__init__(title=title, timeout=None)

    async def on_submit(self, interaction: Interaction, /) -> None:
        await interaction.response.defer()

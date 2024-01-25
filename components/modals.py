import discord
from discord.ui import Modal, TextInput, Select
from discord import TextStyle, Interaction


class NewSeedModal(Modal):
    sotwname = TextInput(
        label="Enter the name for the Seed of the Week",
        style=TextStyle.short,
    )

    sotwdesc = TextInput(
        label="Enter a description for the seed",
        style=TextStyle.paragraph,
    )

    sotwsubmitter = TextInput(
        label="Who submitted this one?",
        style=TextStyle.short,
    )

    sotwflags = TextInput(
        label="Enter the flags",
        style=TextStyle.paragraph,
    )

    def __init__(self, title: str) -> None:
        super().__init__(title=title, timeout=None)

    async def on_submit(self, interaction: Interaction, /) -> None:
        await interaction.response.defer()

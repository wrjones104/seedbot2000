import os
from typing import Literal

import discord
from discord import app_commands, Interaction
from dotenv import load_dotenv

import components.views as views
import parse_commands
from func import command_functions as cf

load_dotenv()


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def setup_hook(self) -> None:
        self.add_view(views.ReRollView(""))
        self.add_view(views.ReRollExtraView("", ""))

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"We have logged in as {self.user}.")


client = aclient()
tree = app_commands.CommandTree(client)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!"):
        await parse_commands.parse_bot_command(message, None, False)


@tree.command(name="help", description="SeedBot help")
@app_commands.describe(type='What do you want help with?')
async def help(interaction: Interaction, type: Literal['general', 'presets', 'dev']):
    if type == 'presets':
        await cf.preset_help(interaction)
    elif type == 'dev':
        await cf.dev_help(interaction)
    else:
        await cf.gen_help(interaction)


client.run(os.getenv('DISCORD_TOKEN'))

import os

import discord
from typing import Literal
from discord import app_commands, Interaction, TextStyle
from discord.ui import Modal, TextInput
from dotenv import load_dotenv
from func import command_functions as cf
import parse_commands

load_dotenv()


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"We have logged in as {self.user}.")


client = aclient()
tree = app_commands.CommandTree(client)


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

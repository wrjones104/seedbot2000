import os
from typing import Literal
import datetime

import discord
from discord import app_commands, Interaction
from discord.ext import commands
from dotenv import load_dotenv

import components.views as views
import parse_commands
from func import command_functions as cf

load_dotenv()


class abot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())
        self.synced = False

    async def setup_hook(self) -> None:
        self.add_view(views.ReRollView(""))
        self.add_view(views.ReRollExtraView("", ""))

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await bot.tree.sync()
            self.synced = True
        print(f"We have logged in as {self.user}.")


bot = abot()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("!"):
        print(f'{datetime.datetime.now()}: {message.author}: {message.content}')
        await parse_commands.parse_bot_command(message, None, False)


@bot.tree.command(name="help", description="SeedBot help")
@app_commands.describe(type='What do you want help with?')
async def sbhelp(interaction: Interaction, type: Literal['general', 'presets', 'dev']):
    if type == 'presets':
        await cf.preset_help(interaction)
    elif type == 'dev':
        await cf.dev_help(interaction)
    else:
        await cf.gen_help(interaction)


bot.run(os.getenv('DISCORD_TOKEN'))

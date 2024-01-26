import datetime
import os
import platform
import sys
from typing import Literal

import discord
from discord import app_commands, Interaction
from discord.ext import commands
from dotenv import load_dotenv

import components.views as views
import functions
import parse_commands
from func import command_functions as cf
from functions import init_db

load_dotenv()


class abot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        self.add_view(views.ReRollView(""))
        self.add_view(views.ReRollExtraView("", ""))

    async def on_ready(self):
        await self.wait_until_ready()
        print(f"{datetime.datetime.utcnow()} - Logged in as " + bot.user.name)
        print(f"{datetime.datetime.utcnow()} - Bot ID: " + str(bot.user.id))
        print(f"{datetime.datetime.utcnow()} - Discord Version: " + discord.__version__)
        print(f"{datetime.datetime.utcnow()} - Python Version: " + str(platform.python_version()))
        synclist = await bot.tree.sync()
        print(f"{datetime.datetime.utcnow()} - Slash Commands Synced: " + str(len(synclist)))
        init_db()
        print(f"{datetime.datetime.utcnow()} - Databases Initialized!")

def check_admin(interaction):
    for x in interaction.user.roles:
        if x.name in ["Racebot Admin", "Moderation team", "Admins"]:
            return True


def restart_bot():
    os.execv(sys.executable, ['python3'] + sys.argv)


bot = abot()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("!"):
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


@bot.tree.command(name="restart", description="Restart the bot if it's having trouble (limited to certain roles)")
async def restart(interaction: discord.Interaction):
    if check_admin(interaction):
        await interaction.response.send_message('Restarting bot...')
        restart_bot()
    else:
        await interaction.response.send_message("Only Admins, Moderators and Racebot Admins can use that command!",
                                                ephemeral=True)


try:
    bot.run(os.getenv('DISCORD_TOKEN'))
except discord.errors.ConnectionClosed as e:
    print(f'{datetime.datetime.utcnow}: Restarting bot due to {e}')
    restart_bot()

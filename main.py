import datetime
import os
import platform

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv

import components.views as views
from functions import init_db, get_buttons, get_views

load_dotenv()


class abot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        self.add_view(
            views.ReRollExtraView(None, None, None, None, None, None, None)
        )
        init_db()
        persistentviews = get_views() 
        for x in persistentviews:
            self.add_view(views.ButtonView(get_buttons(x[0])))
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def on_ready(self):
        await self.wait_until_ready()
        print(f"{datetime.datetime.now(datetime.UTC)} - Logged in as " + bot.user.name)
        print(f"{datetime.datetime.now(datetime.UTC)} - Bot ID: " + str(bot.user.id))
        print(f"{datetime.datetime.now(datetime.UTC)} - Discord Version: " + discord.__version__)
        print(
            f"{datetime.datetime.now(datetime.UTC)} - Python Version: "
            + str(platform.python_version())
        )
        synclist = await self.tree.sync()
        print(
            f"{datetime.datetime.now(datetime.UTC)} - Slash Commands Synced: "
            + str(len(synclist))
        )
        print(f"{datetime.datetime.now(datetime.UTC)} - Databases Initialized!")


bot = abot()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


bot.run(os.getenv("DISCORD_TOKEN"))

# In bot/management/commands/run_bot.py

import datetime
import os
import platform
import discord

from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps
from discord.ext import commands
from discord.ext.commands import CommandNotFound

# --- Key Change 1: Imports ---
# Imports for your own files are now absolute from the 'bot' app root.
from bot.components import views
from bot.functions import init_db, get_buttons, get_views

class abot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        init_db()
        persistentviews = get_views()
        for x in persistentviews:
            self.add_view(views.ButtonView(get_buttons(x[0])))

        # --- Key Change 2: Finding the 'cogs' Folder ---
        # This is the robust Django way to find a directory within an app.
        # It will work no matter where you run the manage.py command from.
        bot_app_config = apps.get_app_config('bot')
        cogs_dir = os.path.join(bot_app_config.path, 'cogs')
        
        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py"):
                # --- Key Change 3: Loading Cogs ---
                # The extension name is now a full Python path from the project root.
                await self.load_extension(f"bot.cogs.{filename[:-3]}")

    async def on_ready(self):
        # We can pass the bot instance around, so we refer to `self` instead of the global `bot`
        await self.wait_until_ready()
        print(f"{datetime.datetime.utcnow()} - Logged in as " + self.user.name)
        print(f"{datetime.datetime.utcnow()} - Bot ID: " + str(self.user.id))
        print(f"{datetime.datetime.utcnow()} - Discord Version: " + discord.__version__)
        print(
            f"{datetime.datetime.utcnow()} - Python Version: "
            + str(platform.python_version())
        )
        synclist = await self.tree.sync()
        print(
            f"{datetime.datetime.utcnow()} - Slash Commands Synced: "
            + str(len(synclist))
        )
        print(f"{datetime.datetime.utcnow()} - Databases Initialized!")
        
    # --- Key Change 4: Event Handlers in a Class ---
    # Events like on_command_error are best defined as methods within the bot class itself.
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        raise error


class Command(BaseCommand):
    help = 'Starts the Discord bot'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Discord bot...'))

        bot = abot()
        
        try:
            bot.run(settings.BOT_TOKEN)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Bot is shutting down...'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
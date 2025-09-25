import datetime
import os
import platform
import discord

from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps
from discord.ext import commands
from discord.ext.commands import CommandNotFound

from bot.functions import init_db

class abot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            help_command=None
        )

    async def setup_hook(self) -> None:
        init_db()

        bot_app_config = apps.get_app_config('bot')
        cogs_dir = os.path.join(bot_app_config.path, 'cogs')
        
        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py"):
                await self.load_extension(f"bot.cogs.{filename[:-3]}")

    async def on_ready(self):
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
        
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        raise error
    
    async def on_interaction(self, interaction: discord.Interaction):
        """A custom interaction dispatcher to bypass the broken default one."""
        if not interaction.data or 'custom_id' not in interaction.data:
            return

        custom_id = interaction.data['custom_id']

        # Import handlers locally to prevent circular dependencies
        from bot.components.views import handle_reroll_button_click, handle_extras_button_click

        if custom_id.startswith("persistent_reroll:"):
            print("--- Manually dispatching to reroll handler ---")
            await handle_reroll_button_click(interaction)

        elif custom_id.startswith("persistent_extras:"):
            print("--- Manually dispatching to extras handler ---")
            await handle_extras_button_click(interaction)
    

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
import os
from typing import Literal

import discord
from discord import app_commands, Interaction
from dotenv import load_dotenv
import parse_commands
import components.views as views

from func import command_functions as cf

load_dotenv()


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def setup_hook(self) -> None:
        # Register the persistent view for listening here.
        # Note that this does not send the view to any message.
        # In order to do this you need to first send a message with the View, which is shown below.
        # If you have the message_id you can also pass it as a keyword argument, but for this example
        # we don't have one.
        self.add_view(views.ReRollView(""))
        self.add_view(views.ReRollExtraView("", ""))
        # self.add_view(views.NewPresetView("", "", "", []))
        # self.add_view(views.TryItView("", "", "", []))

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
        await parse_commands.parse_bot_command(message, False, False, False)


@tree.command(name="help", description="SeedBot help")
@app_commands.describe(type='What do you want help with?')
async def help(interaction: Interaction, type: Literal['general', 'presets', 'dev']):
    if type == 'presets':
        await cf.preset_help(interaction)
    elif type == 'dev':
        await cf.dev_help(interaction)
    else:
        await cf.gen_help(interaction)


# @tree.command(name="roll", description="Seed rolling commands")
# @app_commands.describe(type='What type of seed do you want to roll?')
# @app_commands.describe(engine='Do you want to roll on the current stable version or the dev version?')
# @app_commands.describe(extras='Do you want any extras applied?')
# async def roll(interaction: Interaction, type: Literal['random', 'chaos', 'true chaos', 'preset', 'manual'],
#                engine: Literal['current', 'dev'], extras: str):
#     await interaction.response.send_message(
#         f"Howdy {interaction.user}, you want to roll a {type} seed on the {engine} engine with these extras: {extras}")


client.run(os.getenv('DISCORD_TOKEN'))

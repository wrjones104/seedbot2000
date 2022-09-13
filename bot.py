import os

import discord
from dotenv import load_dotenv

import parse_commands

load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!"):
        await parse_commands.parse_bot_command(message)


client.run(os.getenv('DISCORD_TOKEN'))

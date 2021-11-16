import discord
import os


from create import get_chaos
from create import get_truechaos
from create import get_standard
from create import get_cr_seed
from create import get_cr_chaos_seed
from create import get_standard_paint
from create import get_chaos_paint
from create import get_truechaos_paint
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    args = message.content.split(" ")[1:]
    if message.content.startswith('!rando'):
        if 'chaos ' in args:
            stype = "chaos"
        elif 'true_chaos ' or 'chaos ' in args:
            stype = "true_chaos"
        else:
            stype = "standard"

        if '-s ' in args:
            paint = True




client.run(os.getenv('DISCORD_TOKEN'))

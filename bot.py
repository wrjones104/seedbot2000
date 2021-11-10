import discord
import os

import create
from create import get_chaos
from create import get_truechaos
from create import get_standard
from create import get_test
from create import get_cr_seed
from create import get_chaos_test
from create import get_standard_paint
from create import get_standard_test
from create import get_chaos_paint
from create import get_truechaos_paint
from dotenv import load_dotenv
from flags import chaos

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!rando' or message.content == '!randomseed':
        r = get_standard()
        try:
            await message.channel.send("Here's your seed! Have fun!")
            await message.channel.send(r['share_url'])
        except KeyError:
            await message.channel.send("BZZZZZT!!!")
            await message.channel.send("Oops, there was an flagstring error. Dammit, Jones!!")
            await message.channel.send(r['flags'])
            await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

    if message.content == '!chaos':
        r = get_chaos()
        try:
            await message.channel.send("Oh, you're a feisty one, eh?")
            await message.channel.send(r['share_url'])
        except KeyError:
            await message.channel.send("BZZZZZT!!!")
            await message.channel.send("Oops, there was an flagstring error. Dammit, Jones!!")
            await message.channel.send(r['flags'])
            await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

    if message.content == '!truechaos':
        r = get_truechaos()
        try:
            await message.channel.send("So you have chosen death...")
            await message.channel.send(r['share_url'])
        except KeyError:
            await message.channel.send("BZZZZZT!!!")
            await message.channel.send("Oops, there was an flagstring error. Dammit, Jones!!")
            await message.channel.send(r['flags'])
            await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

    if message.content.startswith('!rando -s') or message.content.startswith('!randomseed -s'):
        r = get_standard_paint()
        try:
            await message.channel.send("A random seed with a fresh coat of paint!")
            await message.channel.send(r['share_url'])
        except KeyError:
            await message.channel.send("BZZZZZT!!!")
            await message.channel.send("Oops, there was an flagstring error. Dammit, Jones!!")
            await message.channel.send(r['flags'])
            await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

    if message.content.startswith('!chaos -s'):
        r = get_chaos_paint()
        try:
            await message.channel.send("Does having more colors make it more chaotic?")
            await message.channel.send(r['share_url'])
        except KeyError:
            await message.channel.send("BZZZZZT!!!")
            await message.channel.send("Oops, there was an flagstring error. Dammit, Jones!!")
            await message.channel.send(r['flags'])
            await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

    if message.content.startswith('!truechaos -s'):
        r = get_truechaos_paint()
        try:
            await message.channel.send("You've successfully randomized... well... everything!")
            await message.channel.send(r['share_url'])
        except KeyError:
            await message.channel.send("BZZZZZT!!!")
            await message.channel.send("Oops, there was an flagstring error. Dammit, Jones!!")
            await message.channel.send(r['flags'])
            await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

    if message.content.startswith('!test'):
        arg = float(message.content.split('!test ', 1)[1].split(' ', 1)[0])
        g = get_cr_seed(arg)
        r = g[0]
        m = g[1]
        argmsg = " ".join(["Your final challenge rating:", str(m)])
        try:
            await message.channel.send("Alrighty, let's give it a shot!")
            await message.channel.send(argmsg)
            await message.channel.send(r['share_url'])
        except KeyError:
            await message.channel.send("BZZZZZT!!!")
            await message.channel.send("Oops, there was an flagstring error. Dammit, Jones!!")
            await message.channel.send(r['flags'])
            await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

client.run(os.getenv('DISCORD_TOKEN'))

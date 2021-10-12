import discord
import os
from create import get_chaos
from create import get_truechaos
from create import get_standard
from create import get_test
from create import get_chaos_test
from create import get_standard_paint
from create import get_standard_test
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

    if message.content == '!btest':
        r = get_test()
        await message.channel.send(get_test())
        await message.channel.send(r['share_url'])

    if message.content == '!brando' or message.content == '!brandomseed':
        r = get_standard()
        await message.channel.send("Here's your seed! Have fun!")
        await message.channel.send(r['share_url'])

    if message.content == '!bchaos':
        r = get_chaos()
        await message.channel.send("Oh, you're a feisty one, eh?")
        await message.channel.send(get_chaos_test())
        await message.channel.send(r['share_url'])

    if message.content == '!btruechaos':
        r = get_truechaos()
        await message.channel.send("So you have chosen death...")
        await message.channel.send(r['share_url'])

    if message.content.startswith('!brando -s') or message.content.startswith('!brandomseed -s'):
        r = get_standard_paint()
        await message.channel.send("Here's your seed! Have fun!")
        await message.channel.send(get_standard_test())
        await message.channel.send(r['share_url'])

    if message.content.startswith('!bchaos -s'):
        r = get_chaos_paint()
        await message.channel.send("Oh, you're a feisty one, eh?")
        await message.channel.send(r['share_url'])

    if message.content.startswith('!btruechaos -s'):
        r = get_truechaos_paint()
        await message.channel.send("So you have chosen death...")
        await message.channel.send(r['share_url'])

client.run(os.getenv('DISCORD_TOKEN'))

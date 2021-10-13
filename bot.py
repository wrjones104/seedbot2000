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

    if message.content == '!beta_test':
        r = get_test()
        await message.channel.send(get_test())
        await message.channel.send(r['share_url'])

    if message.content == '!beta_rando' or message.content == '!beta_randomseed':
        r = get_standard()
        await message.channel.send("Here's your seed! Have fun!")
        await message.channel.send(r['share_url'])

    if message.content == '!beta_chaos':
        r = get_chaos()
        await message.channel.send("Oh, you're a feisty one, eh?")
        await message.channel.send(get_chaos_test())
        await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')
        await message.channel.send(r['share_url'])

    if message.content == '!beta_truechaos':
        r = get_truechaos()
        await message.channel.send("So you have chosen death...")
        await message.channel.send(r['share_url'])

    if message.content.startswith('!beta_rando -s') or message.content.startswith('!beta_randomseed -s'):
        r = get_standard_paint()
        await message.channel.send("Here's your seed! Have fun!")
        await message.channel.send(get_standard_test())
        await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')
        await message.channel.send(r['share_url'])

    if message.content.startswith('!beta_chaos -s'):
        r = get_chaos_paint()
        await message.channel.send("Oh, you're a feisty one, eh?")
        await message.channel.send(r['share_url'])

    if message.content.startswith('!beta_truechaos -s'):
        r = get_truechaos_paint()
        await message.channel.send("So you have chosen death...")
        await message.channel.send(r['share_url'])

client.run(os.getenv('DISCORD_TOKEN'))

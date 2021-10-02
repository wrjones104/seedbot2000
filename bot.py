import discord
import os
import requests
import random
from create import rollseed
from create import get_chaos
from create import get_truechaos

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!rando'):
        r=rollseed()
        await message.channel.send("Here's your seed! Have fun!")
        await message.channel.send(r['share_url'])
        #await message.channel.send("And the flags, too:")
        #await message.channel.send(r['flags'])

    if message.content.startswith('!chaos'):
        r = get_chaos()
        await message.channel.send("Oh, you're a feisty one, eh?")
        await message.channel.send(r['share_url'])

    if message.content.startswith('!truechaos'):
        r=get_truechaos()
        await message.channel.send("So you have chosen death...")
        await message.channel.send(r['share_url'])

client.run('ODkyNTYwNjM4OTY5Mjc4NDg0.YVOr3w.a4NquIslq3z4IUNAx0GJRTnuUxQ')
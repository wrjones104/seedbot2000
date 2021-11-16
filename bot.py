import discord
import os


import flags
from create import get_cr_chaos_seed
from dotenv import load_dotenv
from create import generate_random_seed, generate_cr_seed
from custom_sprites_portraits import spraypaint


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
    paint = ""

    if message.content.startswith('!rando'):
        if 'chaos' in args:
            stype = flags.chaos()
            seedmsg = "Here's your chaos seed. Have fun!"
        elif 'true_chaos' in args or 'true chaos' in args:
            stype = flags.true_chaos()
            seedmsg = "Here's your true chaos seed. Have fun!"
        else:
            stype = flags.standard()
            seedmsg = "Here's your standard seed! Have fun!"

        if '-s' in args:
            paint = spraypaint()
        seed = generate_random_seed(stype, paint)
        try:
            await message.author.send(seedmsg)
            await message.author.send(seed['share_url'])
            await message.delete()
        except KeyError:
            await message.author.send("BZZZZZT!!!")
            await message.author.send("Oops, there was an flagstring error. Please send this to Jones:")
            await message.author.send(seed['flags'])
            await message.author.send('------- FLAGS ABOVE FOR DEBUGGING -------')

    if message.content.startswith('!hardchaos'):
        g = get_cr_chaos_seed()
        r = g[0]
        m = g[1]
        argmsg = " ".join(["Your final challenge rating:", str(m)])
        try:
            await message.author.send("It's about to get REAL!")
            await message.author.send(argmsg)
            await message.author.send(r['share_url'])
            if isinstance(message, discord.channel.DMChannel):
                await message.delete()
        except KeyError:
            await message.author.send("BZZZZZT!!!")
            await message.author.send("Oops, there was an flagstring error. Please send this to Jones:")
            await message.author.send(r['flags'])
            await message.author.send('------- FLAGS ABOVE FOR DEBUGGING -------')

    if message.content.startswith('!cr'):
        c_rating = message.content.split(" ")[1:2]
        if '-s' in args:
            paint = spraypaint()
        seed = generate_cr_seed(paint, c_rating)
        r = seed[0]
        m = seed[1]
        argmsg = " ".join(["Your final challenge rating:", str(m)])
        try:
            await message.author.send("Here's your rated seed! Have fun!")
            await message.author.send(argmsg)
            await message.author.send(r['share_url'])
            await message.delete()
        except KeyError:
            await message.author.send("BZZZZZT!!!")
            await message.author.send("Oops, there was an flagstring error. Please send this to Jones:")
            await message.author.send(seed['flags'])
            await message.author.send('------- FLAGS ABOVE FOR DEBUGGING -------')


client.run(os.getenv('DISCORD_TOKEN'))

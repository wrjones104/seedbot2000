import discord
import os
import datetime
from maths import get_cr
import random
import traceback


import flags
from dotenv import load_dotenv
from create import generate_random_seed, generate_cr_seed, generate_hard_chaos_seed, generate_easy_chaos_seed, cr_search
from custom_sprites_portraits import spraypaint



load_dotenv()

client = discord.Client()


def update_metrics(user, setting, server, url):
    f = open("db/metrics.txt", "a")
    writemsg = ''.join([str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")), ": ", user, " requested a ",
                        setting, " seed @ ", server, ". --- ", url, "\n"])
    f.write(writemsg)
    f.close()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    args = message.content.split(" ")[1:]
    paint = ""

    if message.content.startswith('!cr') or message.content.startswith('!rated'):
        try:
            c_rating = message.content.split(" ")[1:2]
            fixedflags = ""
            if '-fixed' in args:
                fixedflags = message.content.split('-fixed ')[1:]
                fixedflags = fixedflags[0]
            if '-s' in args:
                paint = spraypaint()
            seed = cr_search(paint, c_rating, fixedflags)
            r = seed[0]
            m = seed[1]
            argmsg = " ".join(["Challenge rating:", str(m)])
            try:
                if '-race' in args:
                    flagmsg = ''.join(["```!ff6wcflags ", str(r['flags']), "```"])
                    racemsg = ''.join(
                        ["Copy and paste the flags below into the channel! By the way, your challenge rating"
                         " for this flagset is: ", str(m)])
                    await message.channel.send(racemsg)
                    await message.channel.send(flagmsg)
                else:
                    await message.channel.send("Here's your rated seed, have fun!")
                    await message.channel.send(argmsg)
                    await message.channel.send("> {}".format(r['share_url']))
                    await message.channel.send(c_rating)
            except (KeyError, ValueError):
                await message.channel.send("BZZZZZT!!!")
                await message.channel.send("Oops, there was an flagstring error. Please send this to Jones:")
                ermsg = ''.join(["```", r['flags'], "```"])
                await message.channel.send(ermsg)
                await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')
        except IndexError:
            await message.channel.send("There was an error - did you include your challenge rating number?")


client.run(os.getenv('DISCORD_TOKEN'))

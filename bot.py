import os

import discord
from dotenv import load_dotenv

import functions
import streambot
import parse_commands

load_dotenv()
client = discord.Client()

seed_commands = ["!rando", "!randomseed", "!chaos", "!true_chaos", "!jones_special", "!rollseed", "!true", "!jones"]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await streambot.start_stream_list(client)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!") and message.content.split()[0].strip() in seed_commands:
        await parse_commands.parse_seed_command(message)

    args = message.content.split(" ")[1:]

    # Everything below this point is a command for SeedBot. THIS NEEDS SOME SERIOUS CLEANUP!!

    if message.content.startswith("!getmetrics"):
        await message.channel.send(functions.getmetrics())

    # This gives the user a text file with all seeds that SeedBot has rolled for them
    if message.content.startswith("!myseeds"):
        if functions.myseeds(message.author):
            await message.channel.send(f"Hey {message.author.display_name},"
                                       f" here are all of the seeds I've rolled for you:")
            await message.channel.send(file=discord.File(r'db/myseeds.txt'))
        else:
            await message.channel.send(f"Hey {message.author.display_name}, it looks like I haven't rolled any"
                                       f" seeds for you. You can try it out by typing **!rando** or"
                                       f" **!seedhelp** to get more info!")

    # This take a flagstring as an argument and returns a challenge rating by running it through the "get_cr"
    # rating function
    # if message.content.startswith("!rateflags"):
    #     try:
    #         f2r = ' '.join(args)
    #         f2rr = get_cr(f2r)[1]
    #         ratemsg = f"The challenge rating for this flagset is: {str(f2rr)}"
    #         await message.channel.send(ratemsg)
    #     except (KeyError, IndexError, ValueError):
    #         await message.channel.send("BZZZT!! There was an error! Make sure to put your flags after the"
    #                                    " !rateflags command!")

    # This takes a flagstring as the argument and uses it to roll a seed on the FF6WC website. It will return a
    # share link for that seed
    # if message.content.startswith("!rollseed"):
    #     await functions.rollseed(message, args)

    # This gives the user a list of the last X seeds rolled based on their input. The results list excludes
    # anything that was rolled in a test channel
    if message.content.startswith("!last"):
        try:
            await message.channel.send(functions.last(args))
        except discord.errors.HTTPException:
            await message.channel.send(f'Oops, that was too many results to fit into a single Discord message. '
                                       f'Try a lower number please!')

    # This gives the user a helpful message about SeedBot's current functionality and usage parameters
    if message.content.startswith('!seedhelp'):
        seedhelp = open('db/seedhelp.txt').read()
        await message.author.send(seedhelp)


client.run(os.getenv('DISCORD_TOKEN'))

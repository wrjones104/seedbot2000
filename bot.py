import sys
import random
import discord
import flags
import os
import datetime
import json
import http.client
import functions
import run_wc
from bingo.randomize_drops import run_item_rando
from discord.ext import tasks
from maths import get_cr
from dotenv import load_dotenv
from create import generate_random_seed, cr_search, generate_hard_chaos_seed, generate_easy_chaos_seed, getlink, generate_v1_seed
from custom_sprites_portraits import spraypaint

stream_msg = {}
load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # When SeedBot logs in, it's going to prepare all "live stream" channels for the getstreams function by clearing
    # all previous messages from itself and posting an initial message which will act as the "edit" anchor
#     def is_me(m):
#         return m.author == client.user
#     with open('db/suppressed_servers.txt') as f:
#         suppressed_servers = f.readlines()
#     with open('db/streambot_channels.json') as f:
#         streambot_channels = json.load(f)
#     for a in streambot_channels:
#         if str(streambot_channels[a]['server_id']) in suppressed_servers:
#             continue
#         else:
#             clean_channel = client.get_channel(streambot_channels[a]['channel_id'])
#         await clean_channel.purge(check=is_me)
#         await clean_channel.send("Initializing...")
#     getstreams.start()
#
#
# @tasks.loop(minutes=1)
# async def getstreams():
#     # We're just going to load a bunch of files into variables. We're doing this here so that it reads the files on
#     # every loop, which allows us to edit the files while the bot is running. This is helpful for if we want to add
#     # channels, categories or keywords without having to restart the bot.
#     with open('db/game_cats.json') as f:
#         game_cats = json.load(f)
#     with open('db/streambot_channels.json') as f:
#         streambot_channels = json.load(f)
#     with open('db/suppressed_servers.txt') as f:
#         suppressed_servers = f.readlines()
#     global stream_msg
#     streamlist = ''
#     # This next part searches the Twitch API for all categories and keywords that are specified in the
#     # "game_cats.json" file
#     for gc in game_cats:
#         conn = http.client.HTTPSConnection("api.twitch.tv")
#         payload = ''
#         headers = {
#             'Client-ID': os.getenv('client_id'),
#             'Authorization': os.getenv('twitch_token')
#         }
#         conn.request("GET", "/helix/streams?game_id=" + str(gc) + "&first=100", payload, headers)
#         res = conn.getresponse()
#         data = res.read()
#         x = data.decode("utf-8")
#         # Twitch's API requires a refreshed token every 90 days. Chances are, I'm going to forget about this so this
#         # message is a reminder if that happens! :)
#         if "Invalid OAuth token" in x:
#             streamlist = "Twitch OAuth token expired. Tell Jones!"
#             break
#         j = json.loads(x)
#         xx = j['data']
#         if not j['pagination']:
#             empty_page = True
#             pag = ""
#         else:
#             pag = j['pagination']['cursor']
#             empty_page = False
#         # Twitch's API will only return 100 streams max per call along with a "cursor" which you can use in a
#         # follow-up call to get the next 100 streams. This part just loops through all "pages" until it reaches an
#         # empty one (which means it's at the end)
#         while not empty_page:
#             conn.request("GET", "/helix/streams?game_id=" + str(gc) + "&first=100&after="+str(pag), payload, headers)
#             res = conn.getresponse()
#             data = res.read()
#             x = data.decode("utf-8")
#             j = json.loads(x)
#             try:
#                 if not j['pagination']:
#                     empty_page = True
#                     pass
#                 else:
#                     pag = j['pagination']['cursor']
#                     xx += j['data']
#             except KeyError:
#                 print(j)
#         k = len(xx)
#         # This part takes k (the amount of streams returned total) and uses it to iterate through all the returned
#         # streams to find any with keywords from the "game_cats.json" file in the title of the stream
#         while k != 0:
#             if any(ac in xx[k - 1]['title'].lower() for ac in game_cats[gc]['keywords']):
#                 aa = xx[k - 1]
#                 streamlist += f'**{aa["user_name"]}** is streaming! --- <https://twitch.tv/{aa["user_name"]}>\n' \
#                               f'```Title:       {aa["title"].rstrip()}\nCategory:    {aa["game_name"]}\n' \
#                               f'Stream Time: ' \
#                               f'{str(datetime.datetime.utcnow() - datetime.datetime.strptime(aa["started_at"], "%Y-%m-%dT%H:%M:%SZ")).split(".")[0]}```\n'
#             k -= 1
#     streamlistmsg = f'I found some active streams! Show some love by joining in and following FF6WC' \
#                  f' streamers!\n\n' + streamlist
#     # Next, we're going to send the stream list to all the channels in the "streambot_channels.json" file. If there
#     # are no streams, we're going to send a specific message. If the stream list hasn't changed since the last time
#     # we checked, we're not going to do anything
#     for sc in streambot_channels:
#         if str(streambot_channels[sc]['server_id']) in suppressed_servers:
#             continue
#         else:
#             channel = client.get_channel(streambot_channels[sc]['channel_id'])
#         if channel.id not in stream_msg.keys():
#             stream_msg[channel.id] = await channel.fetch_message(channel.last_message_id)
#         if streamlist == '':
#             await stream_msg[channel.id].edit(content=functions.sad_day())
#             f = open('db/gs_msg.txt', 'w')
#             f.write(functions.sad_day())
#             f.close()
#         elif streamlist == stream_msg[channel.id]:
#             pass
#         else:
#             await stream_msg[channel.id].edit(content=streamlistmsg)
#             f = open('db/gs_msg.txt', 'w')
#             f.write(streamlistmsg)
#             f.close()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Everything below this point is a command for SeedBot. THIS NEEDS SOME SERIOUS CLEANUP!!

    # We're going to start by
    # checking to see if the message we received came from a suppressed server. There's really no use for this yet,
    # but I'm preparing for situations where we might need to suppress commands on a specific server
    with open('db/suppressed_servers.txt') as f:
        suppressed_servers = f.readlines()
    if message.guild.id in suppressed_servers:
        pass
    else:
        args = message.content.split(" ")[1:]
        paint = ""

        if message.content.startswith("!randomseed"):
            try:
                await message.channel.send(functions.randomseed(args))
            except KeyError:
                await message.channel.send("I wasn't able to generate that seed!")

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
        if message.content.startswith("!rateflags"):
            try:
                f2r = ' '.join(args)
                f2rr = get_cr(f2r)[1]
                ratemsg = f"The challenge rating for this flagset is: {str(f2rr)}"
                await message.channel.send(ratemsg)
            except (KeyError, IndexError, ValueError):
                await message.channel.send("BZZZT!! There was an error! Make sure to put your flags after the"
                                           " !rateflags command!")

        # This takes a flagstring as the argument and uses it to roll a seed on the FF6WC website. It will return a
        # share link for that seed
        if message.content.startswith("!rollseed"):
            await message.channel.send(functions.rollseed(args))

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
            await message.channel.send(seedhelp)

        if message.content.startswith("!getstreams"):
            f = open('db/gs_msg.txt')
            await message.channel.send(f.read())
            f.close()

        if message.content.startswith('!jones special'):
            try:
                filename = ''.join(["jones_special_", str(random.randint(1, 99999))])
                run_wc.local_wc(run_wc.flagstrings["jones_special"], filename)
                if "-loot" in args:
                    run_item_rando()
                    await message.channel.send(file=discord.File(r'bingo/roms/lootsplosion.smc', filename=filename+"_lootsplosion.smc"))
                else:
                    await message.channel.send(file=discord.File(r'../worldscollide/zips/'+filename+'.zip'))
                    os.remove('../worldscollide/zips/'+filename+'.zip')
            except AttributeError:
                await message.channel.send("There was a problem generating this seed - please try again!")

        if message.content.startswith('!standard'):
            try:
                filename = ''.join(["standard_race_", str(random.randint(1, 99999))])
                run_wc.local_wc(run_wc.flagstrings["standard_race"], filename)
                if "-loot" in args:
                    run_item_rando()
                    await message.channel.send(file=discord.File(r'bingo/roms/lootsplosion.smc', filename=filename+"_lootsplosion.smc"))
                else:
                    await message.channel.send(file=discord.File(r'../worldscollide/zips/'+filename+'.zip'))
                    os.remove('../worldscollide/zips/'+filename+'.zip')
            except AttributeError:
                await message.channel.send("There was a problem generating this seed - please try again!")

        if message.content.startswith('!aj'):
            try:
                filename = ''.join(["aj_special_", str(random.randint(1, 99999))])
                run_wc.local_wc(run_wc.flagstrings["aj_special"], filename)
                if "-loot" in args:
                    run_item_rando()
                    await message.channel.send(file=discord.File(r'bingo/roms/lootsplosion.smc', filename=filename+"_lootsplosion.smc"))
                else:
                    await message.channel.send(file=discord.File(r'../worldscollide/zips/'+filename+'.zip'))
                    os.remove('../worldscollide/zips/'+filename+'.zip')
            except AttributeError:
                await message.channel.send("There was a problem generating this seed - please try again!")

        if message.content.startswith('!loot'):
            try:
                run_wc.local_wc(run_wc.flagstrings["loot"], "lootsplosion")
                run_item_rando()
                smcfn = 'lootsplosion_' + str(random.randint(1, 9999)) + '.smc'
                await message.channel.send(file=discord.File(r'bingo/roms/lootsplosion.smc', filename=smcfn))
            except AttributeError:
                await message.channel.send("There was a problem generating this seed - please try again!")

        if message.content.startswith('!v1'):
            try:
                await message.channel.send(generate_v1_seed(run_wc.flagstrings['standard_race'])["url"])
            except:
                await message.channel.send("API Error")


client.run(os.getenv('DISCORD_TOKEN'))

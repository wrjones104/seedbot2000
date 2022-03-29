import os
import copy

import json
import http.client

import discord
from discord.ext import tasks

stream_msg = {}
current_stream_msgs = {}
init_msg = {}
with open('db/game_cats.json') as f:
    gcats = json.load(f)
    sad_day = f"I can't find any FF6WC streams right now. In order for me to find streams, the title must reference " \
              f"FF6WC in some way.\n--------------------------------------------\nMy current keywords for the" \
              f" **Final Fantasy VI** category are:" \
              f" {', '.join(gcats['858043689']['keywords'])}\n\nMy current keywords for the **Retro** category" \
              f" are: {', '.join(gcats['27284']['keywords'])}"


async def start_stream_list(client):
    # When SeedBot logs in, it's going to prepare all "live stream" channels by clearing
    # all previous messages from itself and posting an initial message which will act as the "edit" anchor
    await purge_channels(client)
    getstreams.start(client)


async def purge_channels(client):
    def is_me(m):
        return m.author == client.user
    with open('db/streambot_channels.json') as c:
        streambot_channels = json.load(c)
    for a in streambot_channels:
        try:
            clean_channel = client.get_channel(streambot_channels[a]['channel_id'])
            await clean_channel.purge(check=is_me)
            init_msg[clean_channel] = await clean_channel.send("Initializing...")
        except AttributeError:
            print("dang")
            continue


@tasks.loop(minutes=1)
async def getstreams(client):
    # We're just going to load a bunch of files into variables. We're doing this here so that it reads the files on
    # every loop, which allows us to edit the files while the bot is running. This is helpful for if we want to add
    # channels, categories or keywords without having to restart the bot.
    with open('db/game_cats.json') as gc:
        game_cats = json.load(gc)
    with open('db/streambot_channels.json') as sc:
        streambot_channels = json.load(sc)
    global stream_msg
    n_streamlist = {}

    # This next part searches the Twitch API for all categories and keywords that are specified in the
    # "game_cats.json" file
    for gc in game_cats:
        conn = http.client.HTTPSConnection("api.twitch.tv")
        payload = ''
        headers = {
            'Client-ID': os.getenv('client_id'),
            'Authorization': os.getenv('twitch_token')
        }
        conn.request("GET", "/helix/streams?game_id=" + str(gc) + "&first=100", payload, headers)
        res = conn.getresponse()
        data = res.read()
        x = data.decode("utf-8")

        # Twitch's API requires a refreshed token every 90 days. Chances are, I'm going to forget about this so this
        # message is a reminder if that happens! :)
        if "Invalid OAuth token" in x:
            for sc in streambot_channels:
                channel = client.get_channel(streambot_channels[sc]['channel_id'])
                await purge_channels(client)
                await channel.send("BZZZZZZT!!!\n---------------------\nTwitch OAuth token expired. Tell Jones!")
                return getstreams.stop()
            break
        j = json.loads(x)
        xx = j['data']
        if not j['pagination']:
            empty_page = True
            pag = ""
        else:
            pag = j['pagination']['cursor']
            empty_page = False

        # Twitch's API will only return 100 streams max per call along with a "cursor" which you can use in a
        # follow-up call to get the next 100 streams. This part just loops through all "pages" until it reaches an
        # empty one (which means it's at the end)
        while not empty_page:
            conn.request("GET", "/helix/streams?game_id=" + str(gc) + "&first=100&after=" + str(pag), payload, headers)
            res = conn.getresponse()
            data = res.read()
            x = data.decode("utf-8")
            j = json.loads(x)
            try:
                if not j['pagination']:
                    empty_page = True
                    pass
                else:
                    pag = j['pagination']['cursor']
                    xx += j['data']
            except KeyError:
                print(j)
        k = len(xx)

        # This part takes k (the amount of streams returned total) and uses it to iterate through all the returned
        # streams to find any with keywords from the "game_cats.json" file in the title of the stream
        while k != 0:
            if any(ac in xx[k - 1]['title'].lower() for ac in game_cats[gc]['keywords']):
                aa = xx[k - 1]
                index = aa['id']
                n_streamlist[index] = {"user_name": aa["user_name"], "title": aa["title"],
                                       "started_at": aa["started_at"], "category": aa["game_name"]}
            k -= 1

    # Here we're going to create discord messages when a new stream shows up in the list. We're also going to delete
    # messages after a stream has gone offline. Finally, if we go from 0 to >1 active stream (or vice-versa), we're
    # going to edit the initial message
    for x in n_streamlist:
        if any(str(x) in d.values() for d in current_stream_msgs.values()):
            pass
        else:
            for sc in streambot_channels:
                channel = client.get_channel(streambot_channels[sc]['channel_id'])
                embed = discord.Embed()
                embed.title = f'{n_streamlist[x]["user_name"]} is streaming now!'
                embed.url = f'https://twitch.tv/{n_streamlist[x]["user_name"]}'
                embed.description = f'{n_streamlist[x]["title"].strip()}'
                embed.add_field(name="Category", value=n_streamlist[x]["category"])
                embed.colour = discord.Colour.random()
                msg = await channel.send(embed=embed)
                msg_key = '_'.join([str(channel.id), str(x)])
                current_stream_msgs[msg_key] = {"stream_id": x, "msg_id": msg.id, "channel": channel.id}
    for y, v in current_stream_msgs.items():
        if v['stream_id'] not in n_streamlist.keys():
            channel = client.get_channel(v['channel'])
            message = await channel.fetch_message(v['msg_id'])
            await message.delete()
    for k, u in copy.deepcopy(current_stream_msgs).items():
        if u['stream_id'] not in n_streamlist.keys():
            del current_stream_msgs[k]
    if n_streamlist == {}:
        for y, v in init_msg.items():
            await v.edit(content=sad_day)
    else:
        for y, v in init_msg.items():
            await v.edit(content="I found some active streams! Show some love by joining in and following FF6WC"
                                 " streamers!")

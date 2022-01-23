import datetime
import os

import discord
import json
import http.client
from discord.ext import tasks

import functions

stream_msg = {}


async def start_stream_list(client):
    # When SeedBot logs in, it's going to prepare all "live stream" channels for the getstreams function by clearing
    # all previous messages from itself and posting an initial message which will act as the "edit" anchor
    def is_me(m):
        return m.author == client.user
    with open('db/streambot_channels.json') as f:
        streambot_channels = json.load(f)
    for a in streambot_channels:
        clean_channel = client.get_channel(streambot_channels[a]['channel_id'])
        await clean_channel.purge(check=is_me)
        await clean_channel.send("Initializing...")
    getstreams.start(client)


@tasks.loop(minutes=1)
async def getstreams(client):
    # We're just going to load a bunch of files into variables. We're doing this here so that it reads the files on
    # every loop, which allows us to edit the files while the bot is running. This is helpful for if we want to add
    # channels, categories or keywords without having to restart the bot.
    game_cats = json.load(open('db/game_cats.json'))
    streambot_channels = json.load(open('db/streambot_channels.json'))
    global stream_msg
    streamlist = ''
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
            streamlist = "Twitch OAuth token expired. Tell Jones!"
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
                streamlist += f'**{aa["user_name"]}** is streaming! --- <https://twitch.tv/{aa["user_name"]}>\n' \
                              f'```Title:       {aa["title"].rstrip()}\nCategory:    {aa["game_name"]}\n' \
                              f'Stream Time: ' \
                              f'{str(datetime.datetime.utcnow() - datetime.datetime.strptime(aa["started_at"], "%Y-%m-%dT%H:%M:%SZ")).split(".")[0]}```\n'
                index = aa['id']
                n_streamlist[index] = {"user_name": aa["user_name"], "title": aa["title"],
                                       "started_at": aa["started_at"]}
            k -= 1
    streamlistmsg = f'I found some active streams! Show some love by joining in and following FF6WC' \
                    f' streamers!\n\n' + streamlist
    # Next, we're going to send the stream list to all the channels in the "streambot_channels.json" file. If there
    # are no streams, we're going to send a specific message. If the stream list hasn't changed since the last time
    # we checked, we're not going to do anything
    for sc in streambot_channels:
        channel = client.get_channel(streambot_channels[sc]['channel_id'])
        if channel.id not in stream_msg.keys():
            stream_msg[channel.id] = await channel.fetch_message(channel.last_message_id)
        if streamlist == '':
            await stream_msg[channel.id].edit(content=functions.sad_day())
            f = open('db/gs_msg.txt', 'w')
            f.write(functions.sad_day())
            f.close()
        elif streamlist == stream_msg[channel.id]:
            pass
        else:
            await stream_msg[channel.id].edit(content=streamlistmsg)
            f = open('db/gs_msg.txt', 'w')
            f.write(streamlistmsg)
            f.close()
    current_streamers = []
    for x in n_streamlist:
        current_streamers += [n_streamlist[x]["user_name"]]
        print(f'**{n_streamlist[x]["user_name"]}** is streaming now! ---- <https://twitch.tv/{n_streamlist[x]["user_name"]}>\n```Title: {n_streamlist[x]["title"]}\nStreaming Since: {n_streamlist[x]["started_at"]}```')
    print(current_streamers)

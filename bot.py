import discord
import flags
import os
import datetime
import json
import http.client
from discord.ext import tasks
from maths import get_cr
from dotenv import load_dotenv
from functions.functions import create_easiest, create_hardest, create_myseeds, update_metrics, sad_day
from create import generate_random_seed, cr_search, generate_hard_chaos_seed, generate_easy_chaos_seed, getlink
from custom_sprites_portraits import spraypaint

stream_msg = {}
load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # When SeedBot logs in, it's going to prepare all "live stream" channels for the getstreams function by clearing
    # all previous messages from itself and posting an initial message which will act as the "edit" anchor
    def is_me(m):
        return m.author == client.user
    with open('db/suppressed_servers.txt') as f:
        suppressed_servers = f.readlines()
    with open('db/streambot_channels.json') as f:
        streambot_channels = json.load(f)
    for a in streambot_channels:
        if str(streambot_channels[a]['server_id']) in suppressed_servers:
            continue
        else:
            clean_channel = client.get_channel(streambot_channels[a]['channel_id'])
        await clean_channel.purge(check=is_me)
        await clean_channel.send("Initializing...")
    getstreams.start()


@tasks.loop(minutes=1)
async def getstreams():
    # We're just going to load a bunch of files into variables. We're doing this here so that it reads the files on
    # every loop, which allows us to edit the files while the bot is running. This is helpful for if we want to add
    # channels, categories or keywords without having to restart the bot.
    with open('db/game_cats.json') as f:
        game_cats = json.load(f)
    with open('db/streambot_channels.json') as f:
        streambot_channels = json.load(f)
    with open('db/suppressed_servers.txt') as f:
        suppressed_servers = f.readlines()
    global stream_msg
    streamlist = ''
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
        j = json.loads(x)
        xx = j['data']
        pag = j['pagination']['cursor']
        empty_page = False
        # Twitch's API will only return 100 streams max per call along with a "cursor" which you can use in a
        # follow-up call to get the next 100 streams. This part just loops through all "pages" until it reaches an
        # empty one (which means it's at the end)
        while not empty_page:
            conn.request("GET", "/helix/streams?game_id=" + str(gc) + "&first=100&after="+str(pag), payload, headers)
            res = conn.getresponse()
            data = res.read()
            x = data.decode("utf-8")
            j = json.loads(x)
            try:
                if not j['data']:
                    empty_page = True
                    continue
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
                streamlist += f'**{aa["user_name"]}** is streaming: **{aa["title"]}** - ' \
                              f'<https://twitch.tv/{aa["user_name"]}>\n\n'
            k -= 1
    # Next, we're going to send the stream list to all the channels in the "streambot_channels.json" file. If there
    # are no streams, we're going to send a specific message. If the stream list hasn't changed since the last time
    # we checked, we're not going to do anything
    for sc in streambot_channels:
        if str(streambot_channels[sc]['server_id']) in suppressed_servers:
            continue
        else:
            channel = client.get_channel(streambot_channels[sc]['channel_id'])
        if channel.id not in stream_msg.keys():
            stream_msg[channel.id] = await channel.fetch_message(channel.last_message_id)
        if streamlist == '':
            await stream_msg[channel.id].edit(content=sad_day())
            f = open('db/gs_msg.txt', 'w')
            f.write(sad_day())
            f.close()
        elif streamlist == stream_msg[channel.id]:
            pass
        else:
            await stream_msg[channel.id].edit(content=streamlist)
            f = open('db/gs_msg.txt', 'w')
            f.write(streamlist)
            f.close()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    with open('db/suppressed_servers.txt') as f:
        suppressed_servers = f.readlines()

    if message.guild.id in suppressed_servers:
        pass
    else:
        args = message.content.split(" ")[1:]
        paint = ""

        if message.content.startswith('!rando'):
            if 'true_chaos' in args or 'truechaos' in args:
                stype = flags.true_chaos()
                mtype = "true chaos"
                seedmsg = "Here's your true chaos seed. Have fun!"
            elif 'chaos' in args:
                stype = flags.chaos()
                mtype = "chaos"
                seedmsg = "Here's your chaos seed. Have fun!"
            else:
                stype = flags.standard()
                mtype = "standard"
                seedmsg = "Here's your standard seed! Have fun!"

            if '-s' in args:
                paint = spraypaint()
                ptype = True
            else:
                ptype = False

            if '-hundo' in args:
                hundo = True
            else:
                hundo = False
            seed = generate_random_seed(stype, paint, hundo)
            try:
                if '-race' in args:
                    flagmsg = ''.join(["```!ff6wcflags ", str(seed['flags']), "```"])
                    await message.channel.send("Copy and paste the flags below into the channel!")
                    await message.channel.send(flagmsg)
                else:
                    await message.channel.send(seedmsg)
                    await message.channel.send("> {}".format(seed['share_url']))

            except KeyError:
                await message.channel.send("BZZZZZT!!!")
                await message.channel.send("Oops, there was an flagstring error. Please send this to Jones:")
                await message.channel.send("> {}".format(seed['flags']))
                await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')
            try:
                m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
                     "random_sprites": ptype, "request_server": message.guild.name,
                     "request_channel": str(message.channel), "share_url": seed['share_url'],
                     "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
                update_metrics(m)
            except AttributeError:
                m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
                     "random_sprites": ptype, "request_server": "DM",
                     "request_channel": str(message.channel), "share_url": seed['share_url'],
                     "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
                update_metrics(m)

        if message.content.startswith('!chaos'):
            stype = flags.chaos()
            mtype = "chaos"
            seedmsg = "Here's your chaos seed. Have fun!"

            if '-s' in args:
                paint = spraypaint()
                ptype = True
            else:
                ptype = False
            if '-hundo' in args:
                hundo = True
            else:
                hundo = False
            seed = generate_random_seed(stype, paint, hundo)
            try:
                if '-race' in args:
                    flagmsg = ''.join(["```!ff6wcflags ", str(seed['flags']), "```"])
                    await message.channel.send("Copy and paste the flags below into the channel!")
                    await message.channel.send(flagmsg)
                else:
                    await message.channel.send(seedmsg)
                    await message.channel.send("> {}".format(seed['share_url']))

            except KeyError:
                await message.channel.send("BZZZZZT!!!")
                await message.channel.send("Oops, there was an flagstring error. Please send this to Jones:")
                await message.channel.send("> {}".format(seed['flags']))
                await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')
            try:
                m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
                     "random_sprites": ptype, "request_server": message.guild.name,
                     "request_channel": str(message.channel), "share_url": seed['share_url'],
                     "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
                update_metrics(m)
            except AttributeError:
                m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
                     "random_sprites": ptype, "request_server": "DM",
                     "request_channel": str(message.channel), "share_url": seed['share_url'],
                     "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
                update_metrics(m)

        if message.content.startswith('!truechaos') or message.content.startswith('!true_chaos'):
            stype = flags.true_chaos()
            mtype = "true chaos"
            seedmsg = "Here's your true chaos seed. Have fun!"

            if '-s' in args:
                paint = spraypaint()
                ptype = True
            else:
                ptype = False
            if '-hundo' in args:
                hundo = True
            else:
                hundo = False
            seed = generate_random_seed(stype, paint, hundo)
            try:
                if '-race' in args:
                    flagmsg = ''.join(["```!ff6wcflags ", str(seed['flags']), "```"])
                    await message.channel.send("Copy and paste the flags below into the channel!")
                    await message.channel.send(flagmsg)
                else:
                    await message.channel.send(seedmsg)
                    await message.channel.send("> {}".format(seed['share_url']))

            except KeyError:
                await message.channel.send("BZZZZZT!!!")
                await message.channel.send("Oops, there was an flagstring error. Please send this to Jones:")
                await message.channel.send("> {}".format(seed['flags']))
                await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')
            try:
                m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
                     "random_sprites": ptype, "request_server": message.guild.name,
                     "request_channel": str(message.channel), "share_url": seed['share_url'],
                     "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
                update_metrics(m)
            except AttributeError:
                m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
                     "random_sprites": ptype, "request_server": "DM",
                     "request_channel": str(message.channel), "share_url": seed['share_url'],
                     "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
                update_metrics(m)

        if message.content.startswith('!hardchaos'):
            if '-s' in args:
                paint = spraypaint()
                ptype = True
            else:
                ptype = False
            g = generate_hard_chaos_seed(paint)
            mtype = "hard chaos"
            seed = g[0]
            m = g[1]
            argmsg = " ".join(["Challenge rating:", str(m)])
            try:
                if '-race' in args:
                    flagmsg = ''.join(["```!ff6wcflags ", str(seed['flags']), "```"])
                    racemsg = ''.join(
                        ["Copy and paste the flags below into the channel! By the way, your challenge rating"
                         " for this flagset is: ", str(m)])
                    await message.channel.send(racemsg)
                    await message.channel.send(flagmsg)
                else:
                    await message.channel.send("It's about to get REAL!")
                    await message.channel.send(argmsg)
                    await message.channel.send("> {}".format(seed['share_url']))

            except KeyError:
                await message.channel.send("BZZZZZT!!!")
                await message.channel.send("Oops, there was an flagstring error. Please send this to Jones:")
                await message.channel.send("> {}".format(seed['flags']))
                await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')
            try:
                m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
                     "random_sprites": ptype, "request_server": message.guild.name,
                     "request_channel": str(message.channel), "share_url": seed['share_url'],
                     "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
                update_metrics(m)
            except AttributeError:
                m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
                     "random_sprites": ptype, "request_server": "DM",
                     "request_channel": str(message.channel), "share_url": seed['share_url'],
                     "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
                update_metrics(m)

        if message.content.startswith('!easychaos'):
            if '-s' in args:
                paint = spraypaint()
                ptype = True
            else:
                ptype = False
            g = generate_easy_chaos_seed(paint)
            mtype = "easy chaos"
            seed = g[0]
            m = g[1]
            argmsg = " ".join(["Challenge rating:", str(m)])
            try:
                if '-race' in args:
                    flagmsg = ''.join(["```!ff6wcflags ", str(seed['flags']), "```"])
                    racemsg = ''.join(
                        ["Copy and paste the flags below into the channel! By the way, your challenge rating"
                         " for this flagset is: ", str(m)])
                    await message.channel.send(racemsg)
                    await message.channel.send(flagmsg)
                else:
                    await message.channel.send("It's about to get real...easy!")
                    await message.channel.send(argmsg)
                    await message.channel.send("> {}".format(seed['share_url']))

            except KeyError:
                await message.channel.send("BZZZZZT!!!")
                await message.channel.send("Oops, there was an flagstring error. Please send this to Jones:")
                await message.channel.send("> {}".format(seed['flags']))
                await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')
            try:
                m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
                     "random_sprites": ptype, "request_server": message.guild.name,
                     "request_channel": str(message.channel), "share_url": seed['share_url'],
                     "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
                update_metrics(m)
            except AttributeError:
                m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
                     "random_sprites": ptype, "request_server": "DM",
                     "request_channel": str(message.channel), "share_url": seed['share_url'],
                     "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
                update_metrics(m)

        if message.content.startswith('!cr') or message.content.startswith('!rated'):
            try:
                c_rating = message.content.split(" ")[1:2]
                fixedflags = ""
                rangedflags = ""
                mtype = ''.join(["rated (", str(c_rating), ')'])
                if '--fixed' in args:
                    fixedflags = message.content.split('--fixed ')[1:]
                    fixedflags = fixedflags[0].split('--')[0].lstrip()
                    print("fixedflags:", fixedflags)
                if '--ranged' in args:
                    rangedflags = message.content.split('--ranged ')[1:]
                    rangedflags = rangedflags[0].split('--')[0].lstrip()
                    print("rangedflags:", rangedflags)
                if '-s ' in args:
                    paint = spraypaint()
                    ptype = True
                else:
                    ptype = False
                seed = cr_search(paint, c_rating, fixedflags, rangedflags)
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
                except (KeyError, ValueError):
                    await message.channel.send("BZZZZZT!!!")
                    await message.channel.send("Oops, there was an flagstring error. Please send this to Jones:")
                    ermsg = ''.join(["```", r['flags'], "```"])
                    await message.channel.send(ermsg)
                    await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

                try:
                    m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
                         "random_sprites": ptype, "request_server": message.guild.name,
                         "request_channel": str(message.channel), "share_url": r['share_url'],
                         "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
                    update_metrics(m)
                except AttributeError:
                    m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
                         "random_sprites": ptype, "request_server": "DM",
                         "request_channel": str(message.channel), "share_url": r['share_url'],
                         "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
                    update_metrics(m)
            except IndexError:
                await message.channel.send("There was an error - did you include your challenge rating number?")
            except ValueError:
                await message.channel.send("I don't think that's a number...")

        if message.content.startswith("!getmetrics"):
            with open("db/metrics.json") as f:
                counts = {}
                j = json.load(f)
                seedcount = 0
                for k in j:
                    if 'test' not in j[k]['request_channel']:
                        seedcount += 1
                        creator = j[k]['creator_name']
                        if not creator in counts.keys():
                            counts[creator] = 0
                        counts[creator] += 1
                for creator in reversed({k: v for k, v in sorted(counts.items(), key=lambda item: item[1])}):
                    x = ''.join([creator, ": ", str(counts[creator])])
                    # print(creator, counts[creator])
                    # print(x)
                firstseed = j['1']['timestamp']
                creator_counts = []
                for creator in reversed({k: v for k, v in sorted(counts.items(), key=lambda item: item[1])}):
                    creator_counts.append(tuple((creator, counts[creator])))

                top5 = creator_counts[:5]

                # for item in top5:
                #     print(item[0], item[1])
                m_msg = f"Since {firstseed}, I've rolled {seedcount} seeds! The top 5 seed rollers are:\n"
                for roller_seeds in top5:
                    roller = roller_seeds[0]
                    seeds = roller_seeds[1]
                    m_msg += f"> {roller} has rolled {seeds}\n"
                f.close()
                await message.channel.send(m_msg)

        if message.content.startswith("!myseeds"):
            with open("db/metrics.json") as f:
                j = json.load(f)
                x = ""
                for k in j:
                    if message.author.id == j[k]['creator_id']:
                        x += f'{j[k]["timestamp"]}: {j[k]["seed_type"]} @ {j[k]["share_url"]}\n'
                f.close()
                if x != "":
                    create_myseeds(x)
                    await message.channel.send(f"Hey {message.author.display_name},"
                                               f" here are all of the seeds I've rolled for you:")
                    await message.channel.send(file=discord.File(r'db/myseeds.txt'))
                else:
                    await message.channel.send(f"Hey {message.author.display_name}, it looks like I haven't rolled any"
                                               f" seeds for you. You can try it out by typing **!rando** or"
                                               f" **!seedhelp** to get more info!")

        if message.content.startswith("!rateflags"):
            try:
                f2r = ' '.join(args)
                f2rr = get_cr(f2r)[1]
                ratemsg = f"The challenge rating for this flagset is: {str(f2rr)}"
                await message.channel.send(ratemsg)
            except (KeyError, IndexError, ValueError):
                await message.channel.send("BZZZT!! There was an error! Make sure to put your flags after the"
                                           " !rateflags command!")
                await message.channel.send("Example: !rateflags -cg -ktcr 7 7 -kter 10 10 -stno -sc1 random -sc2 random"
                                           " -sal -eu -fst -brl -slr 1 5 -lmprp 75 125 -lel -srr 3 15 -rnl -rnc -sdr 1 1 "
                                           "-das -dda -dns -com 98989898989898989898989898 -rec1 28 -rec2 23 -xpm 3 -mpm 5 "
                                           "-gpm 5 -nxppd -lsp 2 -hmp 2 -xgp 2 -ase 2 -msl 40 -sed -bbs -be -bnu -res "
                                           "-fer 0 -escr 100 -dgne -wnz -mmnu -cmd -esr 1 5 -ebr 68 -emprp 75 125 -nm1"
                                           " random -rnl1 -rns1 -nm2 random -rnl2 -rns2 -nmmi -smc 3 -ieor 33 -ieror 33 "
                                           "-csb 1 32 -mca -stra -saw -sisr 20 -sprp 75 125 -sdm 4 -npi -ccsr 20 -cms -cor "
                                           "-crr -crvr 255 255 -ari -anca -adeh -nfps -nu -fs -fe -fvd -fr -fj -fbs -fedc "
                                           "-as -ond -rr")

        if message.content.startswith("!rollseed"):
            try:
                seed = getlink(' '.join(args))
                linkmsg = seed['share_url']
                await message.channel.send(linkmsg)
            except TypeError:
                await message.channel.send(' '.join(args))
            except KeyError:
                await message.channel.send("Bzzzt! Invalid flagstring!")

        if message.content.startswith("!last5"):
            with open("db/metrics.json") as f:
                j = json.load(f)
                last = len(j)
                last5 = f'Here are the last 5 seeeds rolled:\n' \
                        f'> {j[str(last)]["creator_name"]} rolled a {j[str(last)]["seed_type"]} seed:' \
                        f' {j[str(last)]["share_url"]}\n' \
                        f'> {j[str(last - 1)]["creator_name"]} rolled a {j[str(last - 1)]["seed_type"]} seed:' \
                        f' {j[str(last - 1)]["share_url"]}\n' \
                        f'> {j[str(last - 2)]["creator_name"]} rolled a {j[str(last - 2)]["seed_type"]} seed:' \
                        f' {j[str(last - 2)]["share_url"]}\n' \
                        f'> {j[str(last - 3)]["creator_name"]} rolled a {j[str(last - 3)]["seed_type"]} seed:' \
                        f' {j[str(last - 3)]["share_url"]}\n' \
                        f'> {j[str(last - 4)]["creator_name"]} rolled a {j[str(last - 4)]["seed_type"]} seed:' \
                        f' {j[str(last - 4)]["share_url"]}'
                await message.channel.send(last5)

        if message.content.startswith("!last10"):
            with open("db/metrics.json") as f:
                j = json.load(f)
                last = len(j)
                last10 = f'Here are the last 10 seeeds rolled:\n' \
                         f'> {j[str(last)]["creator_name"]} rolled a {j[str(last)]["seed_type"]} seed:' \
                         f' {j[str(last)]["share_url"]}\n' \
                         f'> {j[str(last - 1)]["creator_name"]} rolled a {j[str(last - 1)]["seed_type"]} seed:' \
                         f' {j[str(last - 1)]["share_url"]}\n' \
                         f'> {j[str(last - 2)]["creator_name"]} rolled a {j[str(last - 2)]["seed_type"]} seed:' \
                         f' {j[str(last - 2)]["share_url"]}\n' \
                         f'> {j[str(last - 3)]["creator_name"]} rolled a {j[str(last - 3)]["seed_type"]} seed:' \
                         f' {j[str(last - 3)]["share_url"]}\n' \
                         f'> {j[str(last - 4)]["creator_name"]} rolled a {j[str(last - 4)]["seed_type"]} seed:' \
                         f' {j[str(last - 4)]["share_url"]}\n' \
                         f'> {j[str(last - 5)]["creator_name"]} rolled a {j[str(last - 5)]["seed_type"]} seed:' \
                         f' {j[str(last - 5)]["share_url"]}\n' \
                         f'> {j[str(last - 6)]["creator_name"]} rolled a {j[str(last - 6)]["seed_type"]} seed:' \
                         f' {j[str(last - 6)]["share_url"]}\n' \
                         f'> {j[str(last - 7)]["creator_name"]} rolled a {j[str(last - 7)]["seed_type"]} seed:' \
                         f' {j[str(last - 7)]["share_url"]}\n' \
                         f'> {j[str(last - 8)]["creator_name"]} rolled a {j[str(last - 8)]["seed_type"]} seed:' \
                         f' {j[str(last - 8)]["share_url"]}\n' \
                         f'> {j[str(last - 9)]["creator_name"]} rolled a {j[str(last - 9)]["seed_type"]} seed:' \
                         f' {j[str(last - 9)]["share_url"]}'
                await message.channel.send(last10)

        if message.content.startswith('!seedhelp'):
            seedhelp = open('db/seedhelp.txt').read()
            await message.channel.send(seedhelp)

        if message.content.startswith('!hardest') and message.author.id == 197757429948219392:
            create_hardest(' '.join(args))
            await message.channel.send("Got it!")

        if message.content.startswith('!easiest') and message.author.id == 197757429948219392:
            create_easiest(' '.join(args))
            await message.channel.send("Got it!")

        if message.content.startswith('!rollhardest'):
            try:
                with open('db/hardest.txt') as f:
                    seed = getlink(f)
                    linkmsg = seed['share_url']
                    await message.channel.send(linkmsg)
            except TypeError:
                await message.channel.send(' '.join(args))
            except KeyError:
                await message.channel.send("Bzzzt! Invalid flagstring!")

        if message.content.startswith('!rolleasiest'):
            try:
                with open('db/easiest.txt') as f:
                    seed = getlink(f)
                    linkmsg = seed['share_url']
                    await message.channel.send(linkmsg)
            except TypeError:
                await message.channel.send(' '.join(args))
            except KeyError:
                await message.channel.send("Bzzzt! Invalid flagstring!")

        if message.content.startswith("!getstreams"):
            f = open('db/gs_msg.txt')
            await message.channel.send(f.read())
            f.close()


client.run(os.getenv('DISCORD_TOKEN'))

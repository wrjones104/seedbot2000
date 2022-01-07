import discord
from discord.ext import tasks
import os
import datetime
import json
import http.client
from maths import get_cr
import random
import traceback

import flags
from dotenv import load_dotenv
from create import generate_random_seed, cr_search, generate_hard_chaos_seed, generate_easy_chaos_seed, getlink
from custom_sprites_portraits import spraypaint

load_dotenv()

client = discord.Client()


def update_metrics(m):
    m_data = json.load(open('db/metrics.json'))
    index = len(m_data) + 1
    m_data[index] = m
    with open('db/metrics.json', 'w') as update_file:
        update_file.write(json.dumps(m_data))


def create_myseeds(x):
    with open('db/myseeds.txt', 'w') as update_file:
        update_file.write(x)
    update_file.close()


def create_hardest(x):
    with open('db/hardest.txt', 'w') as update_file:
        update_file.write(x)
    update_file.close()


def create_easiest(x):
    with open('db/easiest.txt', 'w') as update_file:
        update_file.write(x)
    update_file.close()


seedhelp = """
__Seed Creation Commands:__

**!randomseed standard** or **!rando** - rolls a seed with light randomization. Perfect for quick pick-up-and-go runs.

**!randomseed chaos** or **!chaos** - if you like your flagsets to be a little more wacky, this one's for you! Much more liberal randomization can lead to some really interesting settings.

**!randomseed true_chaos** or **!true_chaos** - this one randomizes... literally everything... with no weighting whatsoever. Test your FF6WC skill and knowledge... and your patience!

**!rated <number>** - **[EXPERIMENTAL]** returns a seed matching the challenge rating you specified in the <number> argument. Lower numbers = easier seeds. I will find a seed as close to the number you put in as I can.

**!hardchaos** - for those of you who enjoy a challenge, this one serves up a particularly tough chaos seed.

**!easychaos** - same as above, only backwards! Rolls an easy chaos seed.

__Additional arguments (add a space followed by any of these after your command):__

**-s** will randomize sprites/palettes/portraits in different ways (sometimes it's a preset, sometimes it's completely random)
**-hundo** will force 100% requirements (currently only working for standard, chaos and true_chaos seeds)
**-race** will put your flagset in a formatted box for you to copy and paste into race rooms

__Other Commands:__

**!myseeds** - get a list of every seed I've rolled for you.

**!rateflags <flagset>** - **[EXPERIMENTAL]** returns the challenge rating for the specified flagset

**!rollseed <flagset>** - rolls a seed from the specified flagset
"""

streams = ''
wc_aliases = ['ff6wc', 'worlds collide', 'ff6 worlds collide', 'ff6: worlds collide', 'ff6 wc', 'ff6: wc', 'async', 'wc', 'tiny winter', 'winter tourn', 'twt', 'sotw', 'seed of the week', 'living seed', 'draft race']
retro_aliases = ['ff6wc', 'worlds collide', 'ff6 worlds collide', 'ff6: worlds collide', 'ff6 wc', 'ff6:wc' 'async', 'wc']
sad_day = f"I can't find any FF6WC streams right now. In order for me to find streams, the title must reference FF6WC " \
          f"in some way.\n--------\nMy current keywords for the **Final Fantasy VI** category are: {', '.join(wc_aliases)}\n\nMy current keywords for the **Retro** category are: {', '.join(retro_aliases)}"

@tasks.loop(minutes=1)
async def getstreams(stream_msg):
    channel = client.get_channel(928713857818570834)
    conn = http.client.HTTPSConnection("api.twitch.tv")
    payload = ''
    headers = {
        'Client-ID': os.getenv('client_id'),
        'Authorization': os.getenv('twitch_token')
    }
    conn.request("GET", "/helix/streams?game_id=858043689&first=100", payload, headers)
    res = conn.getresponse()
    data = res.read()
    x = data.decode("utf-8")
    conn = http.client.HTTPSConnection("api.twitch.tv")
    payload = ''
    headers = {
        'Client-ID': os.getenv('client_id'),
        'Authorization': os.getenv('twitch_token')
    }
    conn.request("GET", "/helix/streams?game_id=858043689&first=100", payload, headers)
    retro_res = conn.getresponse()
    retro_data = retro_res.read()
    retro_x = retro_data.decode("utf-8")
    global streams
    newstreams = ''
    try:
        j = json.loads(x)
        retro_j = json.loads(retro_x)
        # print(j)
        # print(len(j['data']))
        # print(j['data'][1]['title'])
        xx = j['data']
        retro_xx = retro_j['data']
        k = len(xx)
        retro_k = len(retro_xx)
        while k != 0:
            if any(ac in xx[k - 1]['title'].lower() for ac in wc_aliases):
                aa = xx[k - 1]
                # print(xx[k - 1])
                newstreams += f'**{aa["user_name"]}** is streaming: **{aa["title"]}** - <https://twitch.tv/{aa["user_name"]}>\n\n'
            k -= 1
            # print(newstreams)
        while retro_k != 0:
            if any(ac in xx[retro_k - 1]['title'].lower() for ac in wc_aliases):
                aa = retro_xx[retro_k - 1]
                # print(xx[k - 1])
                newstreams += f'**{aa["user_name"]}** is streaming: **{aa["title"]}** - <https://twitch.tv/{aa["user_name"]}>\n\n'
            retro_k -= 1
        if newstreams == '':
            newstreams = sad_day
    except json.decoder.JSONDecodeError:
        await channel.send("ERROR!")
    if newstreams == streams:
        # print("no new streams")
        pass
    else:
        streams = newstreams
        # print(stream_msg)
        await stream_msg.edit(content=streams)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    clean_channel = client.get_channel(928713857818570834)
    def is_me(m):
        return m.author == client.user
    await clean_channel.purge(check=is_me)
    await clean_channel.send('Initializing...')
    stream_msg = await clean_channel.fetch_message(clean_channel.last_message_id)
    getstreams.start(stream_msg)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

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
                racemsg = ''.join(["Copy and paste the flags below into the channel! By the way, your challenge rating"
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
                racemsg = ''.join(["Copy and paste the flags below into the channel! By the way, your challenge rating"
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
        if message.guild.id == 666661907628949504:
            if message.channel.id == 675887103153799209:
                await message.channel.send(streams)
            else:
                pass
        else:
            await message.channel.send(streams)


client.run(os.getenv('DISCORD_TOKEN'))

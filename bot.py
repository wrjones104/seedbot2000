import discord
import os
import datetime
import json
from maths import get_cr


import flags
from dotenv import load_dotenv
from create import generate_random_seed, generate_cr_seed, generate_hard_chaos_seed, generate_easy_chaos_seed, getlink
from custom_sprites_portraits import spraypaint


load_dotenv()

client = discord.Client()


# def update_metrics(user, setting, server, url):
#     f = open("db/metrics.txt", "a")
#     writemsg = ''.join([str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")), ": ", user, " requested a ",
#                         setting, " seed @ ", server, ". --- ", url, "\n"])
#     f.write(writemsg)
#     f.close()

def update_metrics(m):
    m_data = json.load(open('db/metrics.json'))
    index = len(m_data) + 1
    m_data[index] = m
    with open('db/metrics.json', 'w') as update_file:
        update_file.write(json.dumps(m_data))

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
        if 'true_chaos' in args or 'truechaos' in args:
            stype = flags.true_chaos()
            mtype = "truechaos"
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
        seed = generate_random_seed(stype, paint)
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
        m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
             "request_channel": str(message.channel), "share_url": seed['share_url'],
             "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
        update_metrics(m)
        # update_metrics(str(message.author), mtype, str(message.channel), seed['share_url'])

    if message.content.startswith('!chaos'):
        stype = flags.chaos()
        seedmsg = "Here's your chaos seed. Have fun!"

        if '-s' in args:
            paint = spraypaint()
        seed = generate_random_seed(stype, paint)
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

        m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": "chaos",
             "request_channel": str(message.channel), "share_url": seed['share_url'],
             "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
        update_metrics(m)
        # update_metrics(str(message.author), "chaos", str(message.channel), seed['share_url'])

    if message.content.startswith('!truechaos') or message.content.startswith('!true_chaos'):
        stype = flags.true_chaos()
        seedmsg = "Here's your true chaos seed. Have fun!"

        if '-s' in args:
            paint = spraypaint()
        seed = generate_random_seed(stype, paint)
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

        m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": "true chaos",
             "request_channel": str(message.channel), "share_url": seed['share_url'],
             "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
        update_metrics(m)
        # update_metrics(str(message.author), "truechaos", str(message.channel), seed['share_url'])

    if message.content.startswith('!hardchaos'):
        if '-s' in args:
            paint = spraypaint()
        g = generate_hard_chaos_seed(paint)
        r = g[0]
        m = g[1]
        argmsg = " ".join(["Challenge rating:", str(m)])
        try:
            if '-race' in args:
                flagmsg = ''.join(["```!ff6wcflags ", str(r['flags']), "```"])
                racemsg = ''.join(["Copy and paste the flags below into the channel! By the way, your challenge rating"
                                   " for this flagset is: ", str(m)])
                await message.channel.send(racemsg)
                await message.channel.send(flagmsg)
            else:
                await message.channel.send("It's about to get REAL!")
                await message.channel.send(argmsg)
                await message.channel.send("> {}".format(r['share_url']))
            
        except KeyError:
            await message.channel.send("BZZZZZT!!!")
            await message.channel.send("Oops, there was an flagstring error. Please send this to Jones:")
            await message.channel.send("> {}".format(r['flags']))
            await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

        m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": "hard chaos",
             "request_channel": str(message.channel), "share_url": r['share_url'],
             "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
        update_metrics(m)
        # update_metrics(str(message.author), "hardchaos", str(message.channel), r['share_url'])

    if message.content.startswith('!easychaos'):
        if '-s' in args:
            paint = spraypaint()
        g = generate_easy_chaos_seed(paint)
        r = g[0]
        m = g[1]
        argmsg = " ".join(["Challenge rating:", str(m)])
        try:
            if '-race' in args:
                flagmsg = ''.join(["```!ff6wcflags ", str(r['flags']), "```"])
                racemsg = ''.join(["Copy and paste the flags below into the channel! By the way, your challenge rating"
                                   " for this flagset is: ", str(m)])
                await message.channel.send(racemsg)
                await message.channel.send(flagmsg)
            else:
                await message.channel.send("It's about to get real...easy!")
                await message.channel.send(argmsg)
                await message.channel.send("> {}".format(r['share_url']))

        except KeyError:
            await message.channel.send("BZZZZZT!!!")
            await message.channel.send("Oops, there was an flagstring error. Please send this to Jones:")
            await message.channel.send("> {}".format(r['flags']))
            await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

        m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": "easy chaos",
             "request_channel": str(message.channel), "share_url": r['share_url'],
             "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
        update_metrics(m)
        # update_metrics(str(message.author), "easychaos", str(message.channel), r['share_url'])

    if message.content.startswith('!cr') or message.content.startswith('!rated'):
        try:
            c_rating = round(float(message.content.split(" ")[1]))
            if '-s' in args:
                paint = spraypaint()
            seed = generate_cr_seed(paint, c_rating)
            r = seed[0]
            m = seed[1]
            argmsg = " ".join(["Challenge rating:", str(m)])
            try:
                if '-race' in args:
                    flagmsg = ''.join(["```!ff6wcflags ", str(r['flags']), "```"])
                    racemsg = ''.join(["Copy and paste the flags below into the channel! By the way, your challenge rating"
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
                await message.channel.send("> {}".format(r['flags']))
                await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')
        except IndexError:
            await message.channel.send("There was an error - did you include your challenge rating number?")
        except ValueError:
            await message.channel.send("I don't think that's a number...")

        try:
            type_w_rate = ''.join(["rated (", str(c_rating), " > ", str(m), ")"])
            m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": type_w_rate,
                 "request_channel": str(message.channel), "share_url": r['share_url'],
                 "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
            update_metrics(m)
        except UnboundLocalError:
            pass
        # update_metrics(str(message.author), type_w_rate, str(message.channel), r['share_url'])

    if message.content.startswith("!getmetrics"):
        with open("db/metrics.json") as f:
            counts = {}
            j = json.load(f)
            for k in j:
                creator = j[k]['creator_name']
                if not creator in counts.keys():
                    counts[creator] = 0
                counts[creator] += 1
            for creator in reversed({k: v for k, v in sorted(counts.items(), key=lambda item: item[1])}):
                x = ''.join([creator, ": ", str(counts[creator])])
                # print(creator, counts[creator])
                # print(x)
            firstseed = j['1']['timestamp']
            seedtotal = str(len(j))
            creator_counts = []
            for creator in reversed({k: v for k, v in sorted(counts.items(), key=lambda item: item[1])}):
                creator_counts.append(tuple((creator, counts[creator])))

            top5 = creator_counts[:5]

            # for item in top5:
            #     print(item[0], item[1])
            m_msg = f"Since {firstseed}, I've rolled {seedtotal} seeds! The top 5 seed rollers are:\n"
            for roller_seeds in top5:
                roller = roller_seeds[0]
                seeds = roller_seeds[1]
                m_msg += f"\t{roller}: {seeds} seeds\n"
            f.close()
            await message.channel.send(m_msg)

    if message.content.startswith("!rateflags"):
        try:
            f2r = ' '.join(args)
            f2rr = get_cr(f2r)[1]
            ratemsg = ' '.join([str(message.author.display_name), "requested a **!rateflags**. The challenge rating for"
                                                                  " this flagset is:", str(f2rr)])
            await message.channel.send(ratemsg)
            await message.delete()
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



    # if message.content.startswith("!test"):
    #     with open("db/test.txt") as f:
    #         test_msg = f.read()
    #         f.close()
    #         await message.channel.send(test_msg)



client.run(os.getenv('DISCORD_TOKEN'))

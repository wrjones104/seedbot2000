import json
import datetime
import os.path
import random
import create
import run_wc
import flags
import discord
from bingo.randomize_drops import run_item_rando
from bingo.steve import steveify
from zipfile import ZipFile


def update_metrics(m):
    if os.path.exists('db/metrics.json'):
        m_data = json.load(open('db/metrics.json'))
        index = len(m_data) + 1
        m_data[index] = m
        with open('db/metrics.json', 'w') as update_file:
            update_file.write(json.dumps(m_data))
    else:
        pass


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


def sad_day():
    game_cats = json.load(open('db/game_cats.json'))
    sad_msg = f"I can't find any FF6WC streams right now. In order for me to find streams, the title must reference " \
              f"FF6WC in some way.\n--------\n"
    for x in game_cats:
        sad_msg += f"My current keywords for the {game_cats[x]['Name']} category are:" \
                   f" {', '.join(game_cats[x]['keywords'])}\n\n"
    return sad_msg


async def rollseed(args, message):
    mtype = "manually_rolled"
    if '&' in ' '.join(args):
        await message.channel.send("Oooh, a special seed! Give me a second to dig that out...")
        flagstring = list(args)
        for x in args:
            if x.startswith('&'):
                flagstring.remove(x)
        retries = 5
        while retries > 0:
            try:
                run_wc.local_wc(' '.join(flagstring))
                retries = 0
            except AttributeError:
                retries -= 1
                pass
        if '&loot' in args:
            run_item_rando()
            mtype += "_lootsplosion"
        if '&steve' in args:
            steveify()
            mtype += "_steve"
        share_url = 'N/A'
        m = {'creator_id': message.author.id, "creator_name": message.author.display_name, "seed_type": mtype,
             "random_sprites": False, "share_url": share_url,
             "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
        update_metrics(m)
        try:
            filename = mtype + '_' + str(random.randint(1, 999999)) + '.zip'
            # create a ZipFile object
            zipObj = ZipFile('../worldscollide/seedbot.zip', 'w')
            # Add multiple files to the zip
            zipObj.write('../worldscollide/seedbot.smc', arcname=filename + '.smc')
            zipObj.write('../worldscollide/seedbot.txt', arcname=filename + '.txt')
            # close the Zip File
            zipObj.close()
            await message.channel.send(file=discord.File(r'../worldscollide/seedbot.zip', filename=filename))
            await message.channel.send("There you go!")
        except AttributeError:
            await message.channel.send("There was a problem generating this seed - please try again!")
        return mtype
    else:
        try:
            seed = create.generate_v1_seed(' '.join(args))
            rollseedmsg = await message.channel.send(seed['url'])
            if message.channel.category.id == 667114993132765184 or message.channel.category.id == 915290246357327962:
                await rollseedmsg.pin()
                await message.channel.edit(topic=rollseedmsg.content)
        except TypeError:
            await message.channel.send("Bzzzt! Invalid flagstring!")
            print(f'rollseed() typeerror args: {args}')
        except KeyError:
            await message.channel.send("Bzzzt! Invalid flagstring!")
            print(f'rollseed() keyerror args: {args}')


def last(args):
    try:
        with open("db/metrics.json") as f:
            j = json.load(f)
            lenmetrics = len(j)
            lenarg = int(args[0])
            print(f'lenarg:{lenarg}, lenmetrics:{lenmetrics}\nj:{j}')
            if lenarg > lenmetrics:
                lastmsg = f"You asked for the last {lenarg} seeds, but I've only rolled {lenmetrics}! Slow down, turbo!"
            elif lenarg <= 0:
                lastmsg = f"I see you, WhoDat."
            else:
                newj = []
                for x in reversed(j):
                    newj.append(j[str(x)])
                counter = 0
                lastmsg = f'Here are the last {lenarg} seeeds rolled:\n'
                while counter < lenarg:
                    lastmsg += f'> {newj[counter]["creator_name"]} rolled a' \
                               f' {newj[counter]["seed_type"]} seed: {newj[counter]["share_url"]}\n '
                    counter += 1
    except (ValueError, IndexError):
        lastmsg = f'Invalid input! Try !last <number>'
    return lastmsg


def myseeds(author):
    with open("db/metrics.json") as f:
        j = json.load(f)
        x = ""
        for k in j:
            if author.id == j[k]['creator_id']:
                x += f'{j[k]["timestamp"]}: {j[k]["seed_type"]} @ {j[k]["share_url"]}\n'
        f.close()
        if x != "":
            create_myseeds(x)
            has_seeds = True
        else:
            has_seeds = False
    return has_seeds


def getmetrics():
    with open("db/metrics.json") as f:
        counts = {}
        j = json.load(f)
        seedcount = 0
        metric_list = []
        for k in j:
            seedcount += 1
            metric_list.append(j[k])
            creator = j[k]['creator_name']
            if not creator in counts.keys():
                counts[creator] = 0
            counts[creator] += 1
        firstseed = j['1']['timestamp']
        creator_counts = []
        for creator in reversed({k: v for k, v in sorted(counts.items(), key=lambda item: item[1])}):
            creator_counts.append(tuple((creator, counts[creator])))
        top5 = creator_counts[:5]
        m_msg = f"Since {firstseed}, I've rolled {seedcount} seeds! The top 5 seed rollers are:\n"
        for roller_seeds in top5:
            roller = roller_seeds[0]
            seeds = roller_seeds[1]
            m_msg += f"> {roller} has rolled {seeds}\n"
        f.close()
    return m_msg


def randomseed(args, author):
    retries = 5
    while retries > 0:
        if args:
            if args[0] in flags.flag_presets.keys():
                flagstring = flags.flag_presets[args[0]]
                mtype = str(args[0])
            elif "true_chaos" in args or "truechaos" in args:
                flagstring = flags.v1_true_chaos()
                mtype = "true_chaos"
            elif "chaos" in args:
                flagstring = flags.v1_chaos()
                mtype = "chaos"
            else:
                flagstring = flags.v1_standard()
                mtype = "standard"
        else:
            flagstring = flags.v1_standard()
            mtype = "standard"
        if '&' in ' '.join(args):
            retries = 5
            while retries > 0:
                try:
                    run_wc.local_wc(flagstring)
                    break
                except AttributeError:
                    retries -= 1
                    pass
            if '&loot' in args:
                run_item_rando()
                mtype += "_lootsplosion"
            if '&steve' in args:
                steveify()
                mtype += "_steve"
            share_url = 'N/A'
            m = {'creator_id': author.id, "creator_name": author.display_name, "seed_type": mtype,
                 "random_sprites": False, "share_url": share_url,
                 "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
            update_metrics(m)
            return mtype
        else:
            # TODO - figure out this stupid hundo thing
            # if "-hundo" in args:
            #     share_url = create.generate_v1_seed(flagstring + "-oa 2.3.3.2.14.14.4.27.27.6.8.8")['url']
            # else:
            #     share_url = create.generate_v1_seed(flagstring)['url']
            retries = 5
            while retries > 0:
                try:
                    share_url = create.generate_v1_seed(flagstring)['url']
                    seedmsg = f"Here's your {mtype} seed!\n{share_url}"
                    m = {'creator_id': author.id, "creator_name": author.display_name, "seed_type": mtype,
                         "random_sprites": False, "share_url": share_url,
                         "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
                    update_metrics(m)
                    return seedmsg
                except AttributeError:
                    raise


async def make_seed(message, args):
    print(f'message: {message}\nargs: {args}')
    if "&" in ' '.join(args):
        await message.channel.send("Oooh, a special seed! Give me a second to dig that out...")
        try:
            filename = randomseed(args, message.author) + '_' + str(random.randint(1, 999999)) + '.zip'
            # create a ZipFile object
            zipObj = ZipFile('../worldscollide/seedbot.zip', 'w')
            # Add multiple files to the zip
            zipObj.write('../worldscollide/seedbot.smc', arcname=filename + '.smc')
            zipObj.write('../worldscollide/seedbot.txt', arcname=filename + '.txt')
            # close the Zip File
            zipObj.close()
            await message.channel.send(file=discord.File(r'../worldscollide/seedbot.zip', filename=filename))
            await message.channel.send("There you go!")
        except AttributeError:
            await message.channel.send("There was a problem generating this seed - please try again!")
    else:
        try:
            await message.channel.send(randomseed(args, message.author))
        except KeyError:
            await message.channel.send("I wasn't able to generate that seed! I blame Jones... just try again!")

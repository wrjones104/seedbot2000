import json
import datetime
import os.path
import random
import create
import run_wc
import flags
import discord
from bingo.randomize_drops import run_item_rando


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


def rollseed(args):
    mtype = "manually_rolled"
    if "&loot" in args:
        flagstring = []
        for x in args:
            if '&' not in x:
                flagstring.append(x)
        try:
            run_wc.local_wc(' '.join(flagstring), "lootsplosion")
            run_item_rando()
            mtype += "_lootsplosion"
        except AttributeError:
            raise
        linkmsg = mtype
    else:
        try:
            seed = create.getlink(' '.join(args))
            linkmsg = seed['share_url']
        except TypeError:
            linkmsg = ' '.join(args)
        except KeyError:
            linkmsg = "Bzzzt! Invalid flagstring!"
    return linkmsg


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
    if "&loot" in args:
        try:
            run_wc.local_wc(flagstring, "lootsplosion")
            run_item_rando()
            mtype += "_lootsplosion"
            share_url = 'N/A'
        except AttributeError:
            raise
        seedmsg = mtype
    else:
        # TODO - figure out this stupid hundo thing
        # if "-hundo" in args:
        #     share_url = create.generate_v1_seed(flagstring + "-oa 2.3.3.2.14.14.4.27.27.6.8.8")['url']
        # else:
        #     share_url = create.generate_v1_seed(flagstring)['url']
        share_url = create.generate_v1_seed(flagstring)['url']
        seedmsg = f"Here's your {mtype} seed!\n{share_url}"
    m = {'creator_id': author.id, "creator_name": author.display_name, "seed_type": mtype,
         "random_sprites": False, "share_url": share_url,
         "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
    update_metrics(m)
    return seedmsg

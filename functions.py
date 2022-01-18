import json
import random
import create
import run_wc
import flags
from bingo.randomize_drops import run_item_rando


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


def sad_day():
    game_cats = json.load(open('db/game_cats.json'))
    sad_msg = f"I can't find any FF6WC streams right now. In order for me to find streams, the title must reference " \
              f"FF6WC in some way.\n--------\n"
    for x in game_cats:
        sad_msg += f"My current keywords for the {game_cats[x]['Name']} category are:" \
                   f" {', '.join(game_cats[x]['keywords'])}\n\n"
    return sad_msg


def rollseed(args):
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
            if lenarg > lenmetrics:
                lastmsg = f"You asked for the last {lenarg} seeds, but I've only rolled {lenmetrics}! Slow down, turbo!"
            elif lenarg <= 0:
                lastmsg = f"I see you, WhoDat."
            else:
                newj = []
                for deltests in reversed(j):
                    if "test" not in j[str(deltests)]["request_channel"]:
                        newj.append(j[str(deltests)])
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
            if 'test' not in j[k]['request_channel']:
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


def randomseed(args):
    seedmsg = []
    print(args)
    if args:
        for x in args:
            if x in flags.flag_presets:
                seedmsg = f"Here's your {x} seed!\n{create.generate_v1_seed(flags.flag_presets[x])['url']}"
            else:
                seedmsg = f"Here's your standard seed!\n{create.generate_v1_seed(flags.v1_standard())['url']}"
    else:
        seedmsg = f"Here's your standard seed!\n{create.generate_v1_seed(flags.v1_standard())['url']}"
    return seedmsg

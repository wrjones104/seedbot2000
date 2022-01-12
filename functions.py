import json
from create import getlink


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
        seed = getlink(' '.join(args))
        linkmsg = seed['share_url']
    except TypeError:
        linkmsg = ' '.join(args)
    except KeyError:
        linkmsg = "Bzzzt! Invalid flagstring!"
    return linkmsg


def last(args):
    with open("db/metrics.json") as f:
        j = json.load(f)
        newj = []
        for deltests in reversed(j):
            if "test" not in j[str(deltests)]["request_channel"]:
                newj.append(j[str(deltests)])
        try:
            lenarg = int(args[0])
            counter = 0
            last = f'Here are the last {lenarg} seeeds rolled:\n'
            while counter < lenarg:
                last += f'> {newj[counter]["creator_name"]} rolled a' \
                        f' {newj[counter]["seed_type"]} seed: {newj[counter]["share_url"]}\n '
                counter += 1
        except:
            last = f'There was an error - make sure to use !last <number>!'
    return last

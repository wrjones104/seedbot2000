import json
import os.path


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
            if ("request_channel" in j[k] and "test" not in j[k]["request_channel"]) or "request_channel" not in j[k]:
                seedcount += 1
                metric_list.append(j[k])
                creator = j[k]['seed_type']
                if not creator in counts.keys():
                    counts[creator] = 0
                counts[creator] += 1
        firstseed = j['1']['timestamp']
        creator_counts = []
        for creator in reversed({k: v for k, v in sorted(counts.items(), key=lambda item: item[1])}):
            creator_counts.append(tuple((creator, counts[creator])))
        top5 = creator_counts[:5]
        m_msg = f"Since {firstseed}, I've rolled {seedcount} seeds! The top 5 seed types are:\n"
        for roller_seeds in top5:
            roller = roller_seeds[0]
            seeds = roller_seeds[1]
            m_msg += f"> **{roller}**: rolled {seeds} times\n"
        f.close()
    return m_msg


async def add_preset(message):
    flagstring = ' '.join(message.content.split("--flags")[1:]).lower().split("--")[0].strip()
    p_name = ' '.join(message.content.split()[1:]).split("--")[0].strip()
    p_id = p_name.lower()
    d_name = ' '.join(message.content.split("--desc")[1:]).split("--")[0].strip()
    if "&" in flagstring:
        return await message.channel.send("Presets don't support additional arguments. Save your preset with __FF6WC"
                                          " flags only__, then you can add arguments when you roll the preset with"
                                          " the **!preset <name>** command later.")
    if not p_name:
        await message.channel.send("Please provide a name for your preset with: **!add <name> --flags <flags> "
                                   "[--desc <optional description>]**")
    else:
        if not os.path.exists('db/user_presets.json'):
            with open('db/user_presets.json', 'w') as newfile:
                newfile.write(json.dumps({}))
        with open('db/user_presets.json') as preset_file:
            preset_dict = json.load(preset_file)
        if p_id in preset_dict.keys():
            await message.channel.send(f"Preset name already exists! Try another name or use **!update_preset"
                                       f" {p_name} --flags <flags> [--desc <optional description>]** to overwrite")
        else:
            preset_dict[p_id] = {"name": p_name, "creator_id": message.author.id, "creator": message.author.name,
                                 "flags": flagstring, "description": d_name}
            with open('db/user_presets.json', 'w') as updatefile:
                updatefile.write(json.dumps(preset_dict))
            await message.channel.send(f"Preset saved successfully! Use the command **!preset {p_name}** to roll it!")


async def update_preset(message):
    flagstring = ' '.join(message.content.split("--flags")[1:]).lower().split("--")[0].strip()
    p_name = ' '.join(message.content.split()[1:]).split("--")[0].strip()
    p_id = p_name.lower()
    d_name = ' '.join(message.content.split("--desc")[1:]).split("--")[0].strip()
    plist = ""
    n = 0
    if "&" in flagstring:
        return await message.channel.send("Presets don't support additional arguments. Save your preset with __FF6WC"
                                          " flags only__, then you can add arguments when you roll the preset with"
                                          " the **!preset <name>** command later.")
    if not p_name:
        await message.channel.send("Please provide a name for your preset with: **!update <name> --flags <flags> "
                                   "[--desc <optional description>]**")
    else:
        if not os.path.exists('db/user_presets.json'):
            with open('db/user_presets.json', 'w') as newfile:
                newfile.write(json.dumps({}))
        with open('db/user_presets.json') as preset_file:
            preset_dict = json.load(preset_file)
        if p_id not in preset_dict.keys():
            await message.channel.send("I couldn't find a preset with that name!")
            for x, y in preset_dict.items():
                if y["creator_id"] == message.author.id:
                    n += 1
                    plist += f'{n}. {x}\nDescription: {y["description"]}\n'
            if plist:
                await message.channel.send(f"Here are all of the presets I have registered for"
                                           f" you:\n```{plist}```")
            else:
                await message.channel.send("I don't have any presets registered for you yet. Use **!add "
                                           "<name> --flags <flags> [--desc <optional description>]** to add a"
                                           " new one.")
        elif preset_dict[p_id]["creator_id"] == message.author.id:
            p_name = preset_dict[p_id]["name"]
            if not flagstring:
                flagstring = preset_dict[p_id]["flags"]
            if not d_name:
                d_name = preset_dict[p_id]["description"]
            preset_dict[p_id] = {"name": p_name, "creator_id": message.author.id, "creator": message.author.name,
                                 "flags": flagstring, "description": d_name}
            with open('db/user_presets.json', 'w') as updatefile:
                updatefile.write(json.dumps(preset_dict))
            await message.channel.send(f"Preset updated successfully! Use the command **!preset {p_name}** to roll it!")
        else:
            await message.channel.send("Sorry, you can't update a preset that you didn't create!")


async def del_preset(message):
    p_name = ' '.join(message.content.split()[1:]).split("--flags")[0].strip()
    p_id = p_name.lower()
    plist = ""
    n = 0
    if not p_name:
        await message.channel.send("Please provide a name for the preset to delete with: **!delete <name>**")
    else:
        if not os.path.exists('db/user_presets.json'):
            with open('db/user_presets.json', 'w') as newfile:
                newfile.write(json.dumps({}))
        with open('db/user_presets.json') as preset_file:
            preset_dict = json.load(preset_file)
        if p_id not in preset_dict.keys():
            await message.channel.send("I couldn't find a preset with that name!")
            for x, y in preset_dict.items():
                if y["creator_id"] == message.author.id:
                    n += 1
                    plist += f'{n}. {x}\nDescription: {y["description"]}\n'
            if plist:
                await message.channel.send(f"Here are all of the presets I have registered for"
                                           f" you:\n```{plist}```")
            else:
                await message.channel.send("I don't have any presets registered for you yet. Use **!add "
                                           "<name> --flags <flags> [--desc <optional description>]** to add a"
                                           " new one.")
        elif preset_dict[p_id]["creator"] == message.author.name:
            preset_dict.pop(p_id)
            with open('db/user_presets.json', 'w') as updatefile:
                updatefile.write(json.dumps(preset_dict))
            await message.channel.send(f"Preset deleted successfully!")
        else:
            await message.channel.send("Sorry, you can't delete a preset that you didn't create!")


async def my_presets(message):
    if not os.path.exists('db/user_presets.json'):
        with open('db/user_presets.json', 'w') as newfile:
            newfile.write(json.dumps({}))
    with open('db/user_presets.json') as checkfile:
        preset_dict = json.load(checkfile)
    plist = ""
    n = 0
    if any(str(message.author.name) in d.values() for d in preset_dict.values()):
        for x, y in preset_dict.items():
            if y['creator_id'] == message.author.id:
                n += 1
                plist += f'{n}. {y["name"]}\nDescription: {y["description"]}\n'
        await message.channel.send(f"Here are all of the presets I have registered for"
                                   f" you:\n```{plist}```")
    else:
        await message.channel.send("I don't have any presets registered for you yet. Use **!add "
                                   "<name> --flags <flags> [--desc <optional description>]** to add a"
                                   " new one.")


async def p_flags(message):
    p_name = ' '.join(message.content.split()[1:])
    p_id = p_name.lower()
    plist = ""
    n = 0
    if not p_name:
        await message.channel.send("Please provide the name for the preset!")
    else:
        if not os.path.exists('db/user_presets.json'):
            with open('db/user_presets.json', 'w') as newfile:
                newfile.write(json.dumps({}))
        with open('db/user_presets.json') as preset_file:
            preset_dict = json.load(preset_file)
        if p_id not in preset_dict.keys():
            await message.channel.send("I couldn't find a preset with that name!")
            for x, y in preset_dict.items():
                if y["creator_id"] == message.author.id:
                    n += 1
                    plist += f'{n}. {y["name"]}\nDescription: {y["description"]}\n'
            if plist:
                await message.channel.send(f"Here are all of the presets I have registered for"
                                           f" you:\n```{plist}```")
            else:
                await message.channel.send("I don't have any presets registered for you yet. Use **!add "
                                           "<name> --flags <flags> [--desc <optional description>]** to add a"
                                           " new one.")
        else:
            with open('db/user_presets.json') as checkfile:
                preset_dict = json.load(checkfile)
                preset = preset_dict[p_id]
            await message.channel.send(f'The flags for **{preset["name"]}** are:\n```{preset["flags"]}```')



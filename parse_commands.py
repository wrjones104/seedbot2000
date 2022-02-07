import datetime
import json
import random
import subprocess
from zipfile import ZipFile

import discord

import create
import custom_sprites_portraits
import flags
import bingo.randomize_drops
import bingo.steve
import run_local
from functions import update_metrics


async def parse_seed_command(message):
    silly = random.choice(open('db/silly_things_for_seedbot_to_say.txt').read().splitlines())
    mtypes = {"true_chaos": flags.v1_true_chaos(), "chaos": flags.v1_chaos(), "standard": flags.v1_standard(),
              "jones_special": flags.flag_presets["jones_special"], "truechaos": flags.v1_true_chaos()}
    local_args = ["loot", "true_loot", "all_pally", "top_tier", "steve", "tunes", "beta"]
    seed_desc = False
    beta = False
    roll_type = "online"

    # First, let's figure out what flags we're rolling
    if message.content.startswith("!rando") or message.content.startswith('!randomseed'):
        mtype = message.content.split()[1]
        if mtype not in mtypes:
            mtype = "standard"
        flagstring = mtypes[mtype]
    elif message.content.startswith("!betaseed"):
        flagstring = ' '.join(message.content.split("&")[:1]).replace("!betaseed", "").strip().lower()
        mtype = "beta"
        beta = True
        share_url = "N/A"
    elif message.content.startswith("!rollseed"):
        flagstring = ' '.join(message.content.split("&")[:1]).replace("!rollseed", "").strip().lower()
        mtype = "manually rolled"
    elif message.content.startswith("!preset"):
        with open('db/user_presets.json') as checkfile:
            preset_dict = json.load(checkfile)
        preset = ' '.join(message.content.split('&')[:1]).replace("!preset", "").strip()
        if preset in preset_dict.keys():
            flagstring = preset_dict[preset]['flags']
            mtype = f"preset_{preset}"
        else:
            return await message.channel.send("That preset doesn't exist!")
    elif message.content.startswith("!shuffle"):
        with open('db/user_presets.json') as checkfile:
            preset_dict = json.load(checkfile)
        random_preset = random.choice(list(preset_dict))
        flagstring = preset_dict[random_preset]['flags']
        mtype = f"random_preset_{random_preset}"
        await message.channel.send(f'**Preset Name**: {random_preset}\n**Created by**:'
                                   f' {preset_dict[random_preset]["creator"]}\n**Description**:'
                                   f' {preset_dict[random_preset]["description"]}')
    elif message.content.startswith("!chaos"):
        flagstring = flags.v1_chaos()
        mtype = "chaos"
    elif message.content.startswith("!true_chaos") or message.content.startswith("!true"):
        flagstring = flags.v1_true_chaos()
        mtype = "true_chaos"
    elif message.content.startswith("!jones_special") or message.content.startswith("!jones"):
        flagstring = flags.flag_presets["jones_special"]
        mtype = "jones_special"
    else:
        mtype = False
        flagstring = False
        pass
    if message.content.split()[0] != "!rollseed" and "&paint" in message.content:
        flagstring += custom_sprites_portraits.paint()
        mtype += "_paint"

    # Next, let's get all the arguments
    args = message.content.split("&")[1:]

    # Next, let's figure out if this seed will be rolled locally or on the website
    if beta:
        roll_type = "local"
    for x in args:
        if x.strip() == "beta":
            beta = True
            roll_type = "local"
            break
        if x.strip() in local_args:
            roll_type = "local"
            break
    for x in args:
        if x.startswith("desc"):
            seed_desc = ' '.join(x.split()[1:])

    # Now let's roll the seed! We'll split this whole thing up between local and online seeds - starting with online
    # first since it's the easiest
    if roll_type == "online":
        try:
            share_url = create.generate_v1_seed(flagstring, seed_desc)['url']
            await message.channel.send(f"Here's your {mtype} seed - {silly}\n"
                                       f"> {share_url}")
        except TypeError:
            await message.channel.send(f'Oops... I hit an error...')

    # Let's move on to the locally rolled stuff
    else:
        local_args = {"loot": bingo.randomize_drops.loot(), "true_loot": bingo.randomize_drops.true_loot(),
                      "all_pally": bingo.randomize_drops.all_pally(), "top_tier": bingo.randomize_drops.top_tiers(),
                      "steve": True}
        await message.channel.send("Oooh, a special seed! Give me a second to dig that out...")
        try:
            run_local.local_wc(flagstring, beta)
        except subprocess.CalledProcessError:
            await message.channel.send("Oops, I hit an error - probably a bad flagset!")
        for x in args:
            if x.strip() not in local_args.keys():
                pass
            if x.strip() == "steve":
                bingo.steve.steveify()
                mtype += "_steve"
            if x.strip() in ("loot", "true_loot", "all_pally", "top_tier"):
                bingo.randomize_drops.run_item_rando(local_args[x.strip()])
                mtype += f'_{x.strip()}'
            if x.strip() == "tunes":
                run_local.local_jdm()
                mtype += f'_tunes'
        share_url = "N/A"
        try:
            filename = mtype + '_' + str(random.randint(1, 999999))
            if beta:
                directory = "../worldscollide-beta/"
            else:
                directory = "../worldscollide/"
            # create a ZipFile object
            zipObj = ZipFile(directory + 'seedbot.zip', 'w')
            # Add multiple files to the zip
            zipObj.write(directory + 'seedbot.smc', arcname=filename + '.smc')
            zipObj.write(directory + 'seedbot.txt', arcname=filename + '.txt')
            # close the Zip File
            zipObj.close()
            zipfilename = filename + ".zip"
            await message.channel.send(file=discord.File(directory + 'seedbot.zip', filename=zipfilename))
            await message.channel.send("There you go!")
        except AttributeError:
            await message.channel.send("There was a problem generating this seed - please try again!")

    # After all that is done, let's add this seed to the metrics file for reporting later
    if "paint" in mtype:
        p_type = True
    else:
        p_type = False
    m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
         "random_sprites": p_type, "share_url": share_url,
         "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))}
    update_metrics(m)


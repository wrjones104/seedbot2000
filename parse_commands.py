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
import functions


async def parse_bot_command(message):
    silly = random.choice(open('db/silly_things_for_seedbot_to_say.txt').read().splitlines())
    mtypes = {"true_chaos": flags.true_chaos(), "chaos": flags.chaos(), "standard": flags.standard(),
              "truechaos": flags.true_chaos()}
    local_args = ["loot", "true_loot", "all_pally", "top_tier", "steve", "tunes", "dev"]
    seed_desc = False
    dev = False
    share_url = "N/A"
    roll_type = "online"
    args = message.content.split(" ")[1:]

    # -----PRESET COMMANDS-----
    if message.content.startswith("!add"):
        return await functions.add_preset(message)

    if message.content.startswith("!update"):
        return await functions.update_preset(message)

    if message.content.startswith("!my_presets") or message.content.startswith("!mypresets"):
        return await functions.my_presets(message)

    if message.content.startswith("!delete"):
        return await functions.del_preset(message)

    if message.content.startswith("!preset_flags") or message.content.startswith("!pflags"):
        return await functions.p_flags(message)

    if message.content.startswith("!presethelp"):
        return await message.author.send(open('db/presethelp.txt').read())

    # -----OTHER NON-SEED-GENERATING COMMANDS-----
    if message.content.startswith("!getmetrics"):
        return await message.channel.send(functions.getmetrics())

    # This gives the user a text file with all seeds that SeedBot has rolled for them
    if message.content.startswith("!myseeds"):
        if functions.myseeds(message.author):
            await message.channel.send(f"Hey {message.author.display_name},"
                                       f" here are all of the seeds I've rolled for you:")
            return await message.channel.send(file=discord.File(r'db/myseeds.txt'))
        else:
            return await message.channel.send(f"Hey {message.author.display_name}, it looks like I haven't rolled any"
                                              f" seeds for you. You can try it out by typing **!rando** or"
                                              f" **!seedhelp** to get more info!")

    # This gives the user a list of the last X seeds rolled based on their input. The results list excludes
    # anything that was rolled in a test channel
    if message.content.startswith("!last"):
        try:
            return await message.channel.send(functions.last(args))
        except discord.errors.HTTPException:
            return await message.channel.send(f'Oops, that was too many results to fit into a single Discord message. '
                                              f'Try a lower number please!')

    # These give the user helpful messages about SeedBot's current functionality and usage parameters
    if message.content.startswith('!seedhelp'):
        seedhelp = open('db/seedhelp.txt').read()
        return await message.author.send(seedhelp)

    if message.content.startswith('!dev_help') or message.content.startswith("!devhelp"):
        return await message.author.send(f"--------------------------------------------\n**All dev functionality is "
                                         f"still being developed and tested.** Have fun with these settings, "
                                         f"but please remember:\n1. Some settings may not make it into an official "
                                         f"release\n2. Bugs are expected - please report them in the #bug-reports "
                                         f"channel (just make sure to let us know they were from a dev seed)\n3. "
                                         f"These settings may update frequently, so please check the **!devhelp** "
                                         f"often!\n--------------------------------------------\n\n"
                                         f"{open('../worldscollide-beta/beta_readme.txt').read()}\n\n "
                                          f"--------------------------------------------\nUse **!devseed "
                                          f"<flags>** to roll a dev flagset. Alternatively, can also add the **&dev** "
                                          f"argument to any existing command or "
                                          f"preset!\n--------------------------------------------")

    # -----SEED-GENERATING COMMANDS-----
    # First, let's figure out what flags we're rolling
    if message.content.startswith("!rando") or message.content.startswith('!randomseed'):
        mtype = message.content.split()[1]
        if mtype not in mtypes:
            mtype = "standard"
        flagstring = mtypes[mtype]
    elif message.content.startswith("!devseed"):
        flagstring = ' '.join(message.content.split("&")[:1]).replace("!devseed", "").strip().lower()
        mtype = "dev"
        dev = True
    elif message.content.startswith("!rollseed"):
        flagstring = ' '.join(message.content.split("&")[:1]).replace("!rollseed", "").strip().lower()
        mtype = "manually rolled"
    elif message.content.startswith("!preset"):
        with open('db/user_presets.json') as checkfile:
            preset_dict = json.load(checkfile)
        preset = ' '.join(message.content.split('&')[:1]).replace("!preset", "").strip().lower()
        if preset in preset_dict.keys():
            flagstring = preset_dict[preset]['flags']
            mtype = f"preset_{preset_dict[preset]['name']}"
            await message.channel.send(f'**Preset Name**: {preset_dict[preset]["name"]}\n**Created By**:'
                                       f' {preset_dict[preset]["creator"]}\n**Description**:'
                                       f' {preset_dict[preset]["description"]}')
        else:
            return await message.channel.send("That preset doesn't exist!")
    elif message.content.startswith("!shuffle"):
        with open('db/user_presets.json') as checkfile:
            preset_dict = json.load(checkfile)
        random_preset = random.choice(list(preset_dict))
        flagstring = preset_dict[random_preset]['flags']
        mtype = f"random_preset_{preset_dict[random_preset]['name']}"
        await message.channel.send(f'**Preset Name**: {preset_dict[random_preset]["name"]}\n**Created By**:'
                                   f' {preset_dict[random_preset]["creator"]}\n**Description**:'
                                   f' {preset_dict[random_preset]["description"]}')
    elif message.content.startswith("!chaos"):
        flagstring = flags.chaos()
        mtype = "chaos"
    elif message.content.startswith("!true_chaos") or message.content.startswith("!true"):
        flagstring = flags.true_chaos()
        mtype = "true_chaos"
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
    if dev:
        roll_type = "local"
    for x in args:
        print(x.strip())
        if x.strip() == "dev":
            dev = True
            roll_type = "local"
            mtype += "_dev"
        if x.strip() in local_args:
            roll_type = "local"
    for x in args:
        if x.startswith("desc"):
            seed_desc = ' '.join(x.split()[1:])

    # Now let's roll the seed! We'll split this whole thing up between local and online seeds - starting with online
    # first since it's the easiest
    if not mtype:
        return
    if roll_type == "online":
        try:
            share_url = create.generate_v1_seed(flagstring, seed_desc)['url']
            await message.channel.send(f"Here's your {mtype} seed - {silly}\n"
                                       f"> {share_url}")
        except TypeError:
            await message.channel.send(f'It looks like the randomizer didn\'t like your flags. Double-check them and '
                                       f'try again!')

    # Let's move on to the locally rolled stuff
    else:
        local_args = {"loot": bingo.randomize_drops.loot(), "true_loot": bingo.randomize_drops.true_loot(),
                      "all_pally": bingo.randomize_drops.all_pally(), "top_tier": bingo.randomize_drops.top_tiers(),
                      "steve": True}
        await message.channel.send("Oooh, a special seed! Give me a second to dig that out...")
        try:
            run_local.local_wc(flagstring, dev)
        except subprocess.CalledProcessError:
            return await message.channel.send("Oops, I hit an error - probably a bad flagset!")
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
        try:
            filename = mtype + '_' + str(random.randint(1, 999999))
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
    functions.update_metrics(m)

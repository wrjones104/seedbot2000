import datetime
import json
import random
import subprocess
from zipfile import ZipFile

import discord

import bingo.randomize_drops
import bingo.steve
import custom_sprites_portraits
import flag_builder
import functions
import run_local

from db.metric_writer import write_gsheets


async def parse_bot_command(message):
    silly = random.choice(open('db/silly_things_for_seedbot_to_say.txt').read().splitlines())
    mtypes = {"true_chaos": flag_builder.true_chaos(), "chaos": flag_builder.chaos(),
              "standard": flag_builder.standard(), "truechaos": flag_builder.true_chaos()}
    local_args = ["loot", "true_loot", "all_pally", "top_tier", "steve", "tunes", "dev", "ctunes"]
    seed_desc = False
    dev = False
    share_url = "N/A"
    roll_type = "online"
    jdm_spoiler = False
    pargs = ""
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
        embed = discord.Embed()
        embed.title = "Preset Help"
        embed.description = open('db/presethelp.txt').read()
        return await message.author.send(embed=embed)

    if message.content.startswith("!allpresets"):
        await functions.all_presets(message)
        return await message.channel.send(file=discord.File(r'db/all_presets.txt'))

    if message.content.startswith("!blamethebot"):
        message.content = functions.blamethebot()
        args = message.content.split(" ")[1:]
        await message.channel.send(f'**Seed Type**: {message.content.split("&")[0]}\n'
                                   f'**Arguments**: {" ".join(args).strip().replace("  ", " ")}')

    # -----OTHER NON-SEED-GENERATING COMMANDS-----
    if message.content.startswith("!invite"):
        return await message.author.send(f"Hey {message.author.display_name}, if you'd like to add me to your own "
                                         f"server, click this "
                                         f"link:\n<https://discord.com/api/oauth2/authorize?client_id=892560638969278484&permissions=1494917180496&scope=bot>")

    if message.content.startswith("!getmetrics") or message.content.startswith("!stats"):
        embed = discord.Embed()
        embed.title = "SeedBot Dashboard"
        embed.url = "https://datastudio.google.com/reporting/dbae224b-b5d1-4dec-ab13-831ce084b7bd/page/DnTrC"
        embed.description = "Click the title above to check out a fun statistical map (I know, right?) of what I've " \
                            "been up to! "
        embed.colour = discord.Colour.random()
        return await message.channel.send(embed=embed)

    # This gives the user a text file with all seeds that SeedBot has rolled for them
    if message.content.startswith("!myseeds"):
        if functions.myseeds(message.author):
            await message.channel.send(f"Hey {message.author.display_name},"
                                       f" here are all of the seeds I've rolled for you (all timestamps in UTC):")
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
        embed = discord.Embed()
        embed.title = "SeedBot Help"
        embed.description = seedhelp
        return await message.author.send(embed=embed)

    if message.content.startswith('!dev_help') or message.content.startswith("!devhelp"):
        await message.author.send(f"--------------------------------------------\n**All dev functionality is "
                                  f"still being developed and tested.** The dev branch is located here: "
                                  f"<https://github.com/asilverthorn/worldscollide/tree/beta>\n\nHave fun with these "
                                  f"settings, "
                                  f"but please remember:\n1. Some settings may not make it into an official "
                                  f"release\n2. Bugs are expected - please report them in the #bug-reports "
                                  f"channel (just make sure to let us know they were from a dev seed)\n3. "
                                  f"These settings may update frequently, so please check the **!devhelp** "
                                  f"often!\n--------------------------------------------\n\n")
        embed_content = open('../worldscollide-beta/beta_readme.md').read()
        devhelp_embed = discord.Embed()
        devhelp_embed.url = "https://github.com/asilverthorn/WorldsCollide/blob/beta/beta_readme.md"
        devhelp_embed.title = "Dev Help"
        devhelp_embed.description = embed_content
        await message.author.send(embed=devhelp_embed)
        return await message.author.send(f"--------------------------------------------\nUse **!devseed "
                                         f"<flags>** to roll a dev flagset. Alternatively, can also add the **&dev** "
                                         f"argument to any existing command or "
                                         f"preset!\n--------------------------------------------")

    # -----SEED-GENERATING COMMANDS-----
    # First, let's figure out what flags we're rolling
    if message.content.startswith(("!rando", "!standard")):
        try:
            mtype = message.content.split()[1]
            if mtype not in mtypes:
                mtype = "standard"
        except IndexError:
            mtype = "standard"
        flagstring = mtypes[mtype]
    elif message.content.startswith("!devseed"):
        flagstring = ' '.join(message.content.split("&")[:1]).replace("!devseed", "").strip()
        mtype = "dev"
        dev = True
    elif message.content.startswith("!rollseed"):
        flagstring = ' '.join(message.content.split("&")[:1]).replace("!rollseed", "").strip()
        mtype = "manually rolled"
    elif message.content.startswith("!preset"):
        with open('db/user_presets.json') as checkfile:
            preset_dict = json.load(checkfile)
        preset = ' '.join(message.content.split('&')[:1]).lower().replace("!preset", "").strip()
        if preset in preset_dict.keys():
            flagstring = preset_dict[preset]['flags']
            try:
                pargs = preset_dict[preset]['arguments']
            except KeyError:
                pass
            mtype = f"preset_{preset_dict[preset]['name']}"
        else:
            return await message.channel.send("That preset doesn't exist!")
    elif message.content.startswith("!shuffle"):
        with open('db/user_presets.json') as checkfile:
            preset_dict = json.load(checkfile)
        preset = random.choice(list(preset_dict))
        flagstring = preset_dict[preset]['flags']
        mtype = f"preset_{preset_dict[preset]['name']}"
    elif message.content.startswith("!chaos"):
        flagstring = flag_builder.chaos()
        mtype = "chaos"
    elif message.content.startswith("!true"):
        flagstring = flag_builder.true_chaos()
        mtype = "true_chaos"
    else:
        mtype = False
        flagstring = False
        pass
    # if message.content.split()[0] != "!rollseed" and "&paint" in message.content:
    #     flagstring += custom_sprites_portraits.paint()
    #     mtype += "_paint"

    # Next, let's get all the arguments
    if pargs:
        args = message.content.split("&")[1:]
        args += pargs.split()
    else:
        args = message.content.split("&")[1:]
    for x in args:
        if x.strip() == "paint":
            flagstring += custom_sprites_portraits.paint()
            mtype += "_paint"
        if x.strip() == "kupo":
            flagstring += " -name KUPEK.KUMAMA.KUPOP.KUSHU.KUKU.KAMOG.KURIN.KURU.KUPO.KUTAN.MOG.KUPAN.KUGOGO.KUMARO " \
                          "-cpor 10.10.10.10.10.10.10.10.10.10.10.10.10.10.14 " \
                          "-cspr 10.10.10.10.10.10.10.10.10.10.10.10.10.10.82.15.10.19.20.82 " \
                          "-cspp 5.5.5.5.5.5.5.5.5.5.5.5.5.5.1.0.6.1.0.3"
            mtype += "_kupo"
        if x.strip() == "hundo":
            split_flags = flagstring.split(" -")
            split_flags[1] = "oa 2.3.3.2.14.14.4.27.27.6.8.8"
            flagstring = ' -'.join(split_flags)
            mtype += "_hundo"
        if x.strip() == "obj":
            split_flags = flagstring.split(" -")
            split_flags[1] = "oa 2.5.5.1.r.1.r.1.r.1.r.1.r.1.r.1.r.1.r"
            flagstring = ' -'.join(split_flags)
            flagstring += " -oy 0.1.1.1.r -ox 0.1.1.1.r -ow 0.1.1.1.r -ov 0.1.1.1.r"
            mtype += "_obj"

    # Next, let's figure out if this seed will be rolled locally or on the website
    if dev:
        roll_type = "local"
    for x in args:
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
    if roll_type == "online" and "preset" in mtype:
        try:
            share_url = functions.generate_v1_seed(flagstring, seed_desc)['url']
            await message.channel.send(f'**Preset Name**: {preset_dict[preset]["name"]}\n**Created By**:'
                                       f' {preset_dict[preset]["creator"]}\n**Description**:'
                                       f' {preset_dict[preset]["description"]}\n**Seed Link**: {share_url}')
        except TypeError:
            print(f'Flagstring Error!\nSeed Type: {mtype}\nFlags:{flagstring}')
            try:
                # print("yes")
                # run_local.local_wc(flagstring, True)

                ######
                local_args = {"loot": bingo.randomize_drops.loot(), "true_loot": bingo.randomize_drops.true_loot(),
                              "all_pally": bingo.randomize_drops.all_pally(),
                              "top_tier": bingo.randomize_drops.top_tiers(),
                              "steve": True}
                await message.channel.send("Oooh, a special seed! Give me a second to dig that out...")
                try:
                    run_local.local_wc(flagstring, True)
                except subprocess.CalledProcessError:
                    return await message.channel.send("Oops, I hit an error - probably a bad flagset!")
                for x in args:
                    print(x)
                    if x.strip() not in local_args.keys():
                        pass
                    if x.strip() == "steve":
                        bingo.steve.steveify(message)
                        mtype += "_steve"
                    if x.strip() in ("loot", "true_loot", "all_pally", "top_tier"):
                        bingo.randomize_drops.run_item_rando(local_args[x.strip()])
                        mtype += f'_{x.strip()}'
                    if x.strip() == "tunes":
                        run_local.local_jdm()
                        mtype += f'_tunes'
                        jdm_spoiler = True
                    if x.strip() == "ctunes":
                        run_local.local_jdc()
                        mtype += f'_ctunes'
                        jdm_spoiler = True
                try:
                    filename = mtype + '_' + str(random.randint(1, 999999))
                    directory = "../worldscollide/"
                    # create a ZipFile object
                    zipObj = ZipFile(directory + 'seedbot.zip', 'w')
                    # Add multiple files to the zip
                    zipObj.write(directory + 'seedbot.smc', arcname=filename + '.smc')
                    zipObj.write(directory + 'seedbot.txt', arcname=filename + '.txt')
                    if jdm_spoiler:
                        zipObj.write("../johnnydmad/spoiler.txt", arcname=filename + "_music_swaps.txt")
                    # close the Zip File
                    zipObj.close()
                    zipfilename = filename + ".zip"
                    if "preset" in mtype:
                        await message.channel.send(f'**Preset Name**: {preset_dict[preset]["name"]}\n**Created By**:'
                                                   f' {preset_dict[preset]["creator"]}\n**Description**:'
                                                   f' {preset_dict[preset]["description"]}')
                    await message.channel.send(file=discord.File(directory + 'seedbot.zip', filename=zipfilename))
                except AttributeError:
                    await message.channel.send("There was a problem generating this seed - please try again!")

                ######
            except subprocess.CalledProcessError:
                print("no")
                return await message.channel.send(f'It looks like the randomizer didn\'t like your flags. Double-check '
                                                  f'them and try again!')
    elif roll_type == "online":
        try:
            share_url = functions.generate_v1_seed(flagstring, seed_desc)['url']
            await message.channel.send(f"Here's your {mtype} seed - {silly}\n"
                                       f"> {share_url}")
        except TypeError:
            print(f'Flagstring Error!\nSeed Type: {mtype}\nFlags:{flagstring}')
            return await message.channel.send(f'It looks like the randomizer didn\'t like your flags. Double-check '
                                              f'them and try again!')

    # Let's move on to the locally rolled stuff
    else:
        local_args = {"loot": bingo.randomize_drops.loot(), "true_loot": bingo.randomize_drops.true_loot(),
                      "all_pally": bingo.randomize_drops.all_pally(), "top_tier": bingo.randomize_drops.top_tiers(),
                      "steve": True}
        await message.channel.send("Oooh, a special seed! Give me a second to dig that out...")
        try:
            run_local.local_wc(flagstring, dev)
        except subprocess.CalledProcessError:
            try:
                run_local.local_wc(flagstring, True)
            except subprocess.CalledProcessError:
                return await message.channel.send("Oops, I  hit an error - probably a bad flagset")
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
                jdm_spoiler = True
            if x.strip() == "ctunes":
                run_local.local_jdc()
                mtype += f'_ctunes'
                jdm_spoiler = True
        try:
            filename = mtype + '_' + str(random.randint(1, 999999))
            directory = "../worldscollide/"
            # create a ZipFile object
            zipObj = ZipFile(directory + 'seedbot.zip', 'w')
            # Add multiple files to the zip
            zipObj.write(directory + 'seedbot.smc', arcname=filename + '.smc')
            zipObj.write(directory + 'seedbot.txt', arcname=filename + '.txt')
            if jdm_spoiler:
                zipObj.write("../johnnydmad/spoiler.txt", arcname=filename + "_music_swaps.txt")
            # close the Zip File
            zipObj.close()
            zipfilename = filename + ".zip"
            if "preset" in mtype:
                await message.channel.send(f'**Preset Name**: {preset_dict[preset]["name"]}\n**Created By**:'
                                           f' {preset_dict[preset]["creator"]}\n**Description**:'
                                           f' {preset_dict[preset]["description"]}')
            await message.channel.send(file=discord.File(directory + 'seedbot.zip', filename=zipfilename))
        except AttributeError:
            await message.channel.send("There was a problem generating this seed - please try again!")

    # After all that is done, let's add this seed to the metrics file for reporting later
    if "paint" in mtype:
        p_type = True
    else:
        p_type = False
    try:
        server_name = message.guild.name
        server_id = message.guild.id
    except AttributeError:
        server_name = "DM"
        server_id = "N/A"
    try:
        channel_name = message.channel.name
        channel_id = message.channel.id
    except AttributeError:
        channel_name = "N/A"
        channel_id = "N/A"
    m = {'creator_id': message.author.id, "creator_name": message.author.name, "seed_type": mtype,
         "random_sprites": p_type, "share_url": share_url,
         "timestamp": str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")), "server_name": server_name,
         "server_id": server_id, "channel_name": channel_name, "channel_id": channel_id}
    functions.update_metrics(m)
    write_gsheets(m)

import datetime
import json
import logging
import random
import re
import subprocess
from zipfile import ZipFile

import discord
import git

import bingo.randomize_drops
import bingo.steve
import components.views as views
import custom_sprites_portraits
import flag_builder
import functions
import run_local
from db.metric_writer import write_gsheets

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

botadmins = [197757429948219392, 462714474562846723, 158251731996770305]
dooradmins = [197757429948219392, 470943697178066944]


async def parse_bot_command(message, reroll_args, reroll):
    silly = random.choice(open('db/silly_things_for_seedbot_to_say.txt').read().splitlines())
    local_args = ["loot", "true_loot", "all_pally", "top_tier", "steve", "tunes", "ctunes", "notunes", "poverty",
                  "Loot", "True Loot", "Poverty", "STEVE", "Tunes", "Chaotic Tunes", "No Tunes",
                  "doors", "dungeoncrawl", "Doors", "Dungeon Crawl", "doors_lite", "Doors Lite"]
    seed_desc = False
    share_url = "N/A"
    roll_type = "online"
    jdm_spoiler = False
    dev = False
    pargs = ""
    mtype = ""
    if reroll:
        args = reroll_args
    else:
        args = message.content.split("&")[1:]

    # -----PRESET COMMANDS-----
    if message.content.startswith("!add "):
        return await functions.add_preset(message)

    if message.content.startswith("!update "):
        return await functions.update_preset(message)

    if message.content.startswith("!my_presets") or message.content.startswith("!mypresets"):
        return await functions.my_presets(message)

    if message.content.startswith("!delete "):
        return await functions.del_preset(message)

    if message.content.startswith("!preset_flags ") or message.content.startswith("!pflags "):
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
        btb = functions.blamethebot(message)
        message.content = btb[0]
        args = message.content.split(" ")[1:]
        mtype = "blamethebot_"
        await message.channel.send(f'**Seed Type**: {message.content.split("&")[0]}\n'
                                   f'**Arguments**: {"".join(btb[1]).strip().replace("  ", " ")}')

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

    # These give the user helpful messages about SeedBot's current functionality and usage parameters
    if message.content.startswith('!seedhelp'):
        seedhelp = open('db/seedhelp.txt').read()
        embed = discord.Embed()
        embed.title = "SeedBot Help"
        embed.description = seedhelp
        return await message.author.send(embed=embed)

    if message.content.startswith('!pinhelp'):
        if message.author.id in botadmins:
            seedhelp = open('db/seedhelp.txt').read()
            embed = discord.Embed()
            embed.title = "SeedBot Help"
            embed.description = seedhelp
            helpmsg = await message.channel.send(embed=embed)
            return await helpmsg.pin()
        else:
            return await message.author.send(f"Sorry, only bot admins can use this command!")

    if message.content.startswith('!betapull') or message.content.startswith('!devpull'):
        try:
            if message.author.id in botadmins:
                g = git.cmd.Git('../worldscollide-beta')
                g.pull()
                return await message.author.send("Pulled!")
            else:
                return await message.author.send(f"Sorry, only bot admins can use this command!")
        except git.exc.GitError:
            return await message.author.send(f"Something went wrong...")

    if message.content.startswith('!doorpull'):
        try:
            if message.author.id in dooradmins:
                g = git.cmd.Git('../wc_door_rando')
                g.pull()
                return await message.author.send("Pulled!")
            else:
                return await message.author.send(f"Sorry, only bot admins can use this command!")
        except git.exc.GitError:
            return await message.author.send(f"Something went wrong...")

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
        try:
            await message.author.send(embed=devhelp_embed)
        except:
            await message.author.send("Check out all of the upcoming dev changes in detail at "
                                      "<https://github.com/asilverthorn/WorldsCollide/blob/beta/beta_readme.md>")
        return await message.author.send(f"--------------------------------------------\nUse **!devseed "
                                         f"<flags>** to roll a dev flagset. Alternatively, can also add the **&dev** "
                                         f"argument to any existing command or "
                                         f"preset!\n--------------------------------------------")

    if message.content.startswith("!version"):
        oldsite = functions.get_vers("old")
        newsite = functions.get_vers("new")
        with open("../worldscollide/version.py") as x:
            smain = re.findall('"([^"]*)"', x.readlines()[0])[0]
        with open("../worldscollide-beta/version.py") as x:
            sdev = re.findall('"([^"]*)"', x.readlines()[0])[0]
        with open("../wc_door_rando/version.py") as x:
            doorv = re.findall('"([^"]*)"', x.readlines()[0])[0]
        await message.channel.send(
            f"**ff6wc.com:** {oldsite['version']}\n**ff6worldscollide.com:** {newsite['version']}\n**SeedBot Main:** {smain}\n**SeedBot Dev:** {sdev}\n**SeedBot Door Rando:** {doorv}")

    # -----SEED-GENERATING COMMANDS-----
    # First, let's figure out what flags we're rolling
    if message.content.startswith(("!rando", "!standard")):
        flagstring = flag_builder.standard()
        mtype += "standard"
    elif message.content.startswith("!devseed"):
        flagstring = ' '.join(message.content.split("&")[:1]).replace("!devseed", "").strip()
        mtype += "dev"
        dev = "dev"
    elif message.content.startswith("!rollseed"):
        flagstring = ' '.join(message.content.split("&")[:1]).replace("!rollseed", "").strip()
        mtype += "manually rolled"
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
            mtype += f"preset_{preset_dict[preset]['name']}"
        else:
            return await message.channel.send("That preset doesn't exist!")
    elif message.content.startswith("!weekly"):
        with open('db/user_presets.json') as checkfile:
            preset_dict = json.load(checkfile)
        try:
            flagstring = preset_dict["ap weekly"]['flags']
            mtype += f"preset_{preset_dict['ap weekly']['name']}"
            args = message.content.split()[1:]
            try:
                if "gat" in args[0]:
                    args = ["ap gat"]
                elif "on" in args[0]:
                    args = ["ap on"]
            except IndexError:
                args = ["ap off"]
        except:
            return await message.channel.send("That preset doesn't exist!")
    elif message.content.startswith("!shuffle"):
        with open('db/user_presets.json') as checkfile:
            preset_dict = json.load(checkfile)
        preset = random.choice(list(preset_dict))
        flagstring = preset_dict[preset]['flags']
        try:
            pargs = preset_dict[preset]['arguments']
        except KeyError:
            pass
        mtype += f"preset_{preset_dict[preset]['name']}"
    elif message.content.startswith("!coliseum"):
        with open('db/user_presets.json') as checkfile:
            preset_dict = json.load(checkfile)
        cololist = []
        for x, y in preset_dict.items():
            try:
                if y['official'] and "coliseum" in y['name']:
                    cololist.append(x)
                else:
                    pass
            except KeyError:
                pass
        if cololist:
            preset = random.choice(cololist)
            flagstring = preset_dict[preset]['flags']
            mtype += f"preset_{preset_dict[preset]['name']}"
        else:
            return await message.channel.send("There are no official coliseum presets right now!")
    elif message.content.startswith("!chaos"):
        flagstring = flag_builder.chaos()
        mtype += "chaos"
    elif message.content.startswith("!true"):
        flagstring = flag_builder.true_chaos()
        mtype += "true_chaos"
    else:
        mtype = False
        flagstring = False
        pass

    # Next, let's get all the arguments
    if pargs and not reroll:
        args += pargs.split()
    for x in args:
        if x.strip().casefold() == "dev":
            dev = "dev"
            mtype += "_dev"
        if x.strip().casefold() == "paint":
            flagstring += custom_sprites_portraits.paint()
            mtype += "_paint"
        if x.strip().casefold() == "kupo":
            flagstring += " -name KUPEK.KUMAMA.KUPOP.KUSHU.KUKU.KAMOG.KURIN.KURU.KUPO.KUTAN.MOG.KUPAN.KUGOGO.KUMARO " \
                          "-cpor 10.10.10.10.10.10.10.10.10.10.10.10.10.10.14 " \
                          "-cspr 10.10.10.10.10.10.10.10.10.10.10.10.10.10.82.15.10.19.20.82 " \
                          "-cspp 5.5.5.5.5.5.5.5.5.5.5.5.5.5.1.0.6.1.0.3"
            mtype += "_kupo"
        if x.strip() in ("fancygau", "Fancy Gau"):
            if "-cspr" in flagstring:
                sprites = flagstring.split('-cspr ')[1].split(' ')[0]
                fancysprites = '.'.join(['.'.join(sprites.split('.')[0:11]), "68", '.'.join(sprites.split('.')[12:20])])
                flagstring = ' '.join([''.join([flagstring.split('-cspr ')[0], "-cspr ", fancysprites]),
                                       ' '.join(flagstring.split('-cspr ')[1].split(' ')[1:])])
            else:
                flagstring += " -cspr 0.1.2.3.4.5.6.7.8.9.10.68.12.13.14.15.18.19.20.21"
            mtype += "_fancygau"
        if x.strip().casefold() == "hundo":
            flagstring += " -oa 2.3.3.2.14.14.4.27.27.6.8.8"
            mtype += "_hundo"
        if x.strip() in ("obj", "Objectives"):
            flagstring += " -oa 2.5.5.1.r.1.r.1.r.1.r.1.r.1.r.1.r.1.r -oy 0.1.1.1.r -ox 0.1.1.1.r -ow 0.1.1.1.r -ov " \
                          "0.1.1.1.r "
            mtype += "_obj"
        if x.strip() in ("nospoiler", "No Spoiler"):
            flagstring = flagstring.replace(" -sl ", " ")
            mtype += "_nospoiler"
        if x.strip() in ("noflashes", "No Flashes"):
            flagstring = ''.join([flagstring.replace(" -frm", "").replace(" -frw", ""), " -frw"])
            mtype += "_noflashes"
        if x.strip().casefold() == "yeet":
            flagstring = ''.join([flagstring.replace(" -ymascot", "").replace(" -ycreature", "").replace(" -yimperial",
                                                                                                         "").replace(
                " -ymain", "").replace(" -yreflect", "").replace(" -ystone", "").replace(" -yvxv", "").replace(
                " -ysketch", "").replace(" -yrandom", "").replace(" -yremove", ""), " -yremove"])
            mtype += "_yeet"
        if x.strip().casefold() == "palette":
            flagstring += custom_sprites_portraits.palette()
            mtype += "_palette"
        if x.strip().casefold() == "mystery":
            flagstring = ''.join([flagstring.replace(" -hf", ""), " -hf"])
            roll_type = "local"
            mtype += "_mystery"
        if x.strip().casefold() == "doors":
            if dev == "dev":
                return await message.channel.send(f"Sorry, door rando doesn't work on dev currently")
            else:
                flagstring += " -dra"
                dev = "doors"
                mtype += "_doors"
        if x.strip() in ("dungeoncrawl", "Dungeon Crawl"):
            if dev == "dev":
                return await message.channel.send(f"Sorry, door rando doesn't work on dev currently")
            else:
                flagstring += " -drdc"
                dev = "doors"
                mtype += "_dungeoncrawl"
        if x.strip() in ("doors_lite", "Doors Lite"):
            if dev == "dev":
                return await message.channel.send(f"Sorry, door rando doesn't work on dev currently")
            else:
                flagstring += " -dre"
                dev = "doors"
                mtype += "_doors_lite"
        if "ap" in x.strip().casefold():
            try:
                ap_args = x.casefold().split("ap ")[1:][0].split()[0]
                if "gat" in ap_args:
                    ap_args = "on_with_additional_gating"
                elif ap_args == "on":
                    ap_args = "on"
                else:
                    ap_args = "off"
            except IndexError:
                ap_args = "off"
            with open('db/template.yaml') as yaml:
                yaml_content = yaml.read()
            flagstring = flagstring.replace("-open", "-cg").replace("-lsced", "-lsc").replace("-lsa",
                                                                                                       "-lsc").replace(
                "-lsh", "-lsc").replace("-lst", "-lsc").replace("-hmced", "-hmc").replace("-hma", "-hmc").replace(
                "-hmh", "-hmc").replace("-hmt", "-hmc").replace("-xgced", "-xgc").replace("-xga", "-xgc").replace(
                "-xgh", "-xgc").replace("-xgt", "-xgc")
            with open("db/ap.yaml", "w", encoding="utf-8") as yaml_file:
                yaml_file.write(yaml_content.replace("flags", flagstring).replace("ts_option", ap_args).replace("Player{number}", ''.join([message.author.display_name, "_WC{number}"])))
            return await message.channel.send(file=discord.File(r'db/ap.yaml', filename=''.join([message.author.display_name, "_WC_", mtype, "_",str(random.randint(0, 65535)),".yaml"])))
        if x.strip().casefold() == "flagsonly":
            return await message.channel.send(f"```{flagstring}```")

    # Next, let's figure out if this seed will be rolled locally or on the website
    for x in args:
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
            share_url = functions.generate_v1_seed(flagstring, seed_desc, dev)['url']
            await message.channel.send(
                f'Here\'s your preset seed - {silly}\n**Preset Name**: {preset_dict[preset]["name"]}\n**Created By**:'
                f' {preset_dict[preset]["creator"]}\n**Description**:'
                f' {preset_dict[preset]["description"]}\n**Seed Link**: <{share_url}>',
                view=views.ReRollView(message))
        except TypeError:
            logging.info(f'Flagstring Error!\nSeed Type: {mtype}\nFlags:{flagstring}')
            try:
                local_args = {"loot": bingo.randomize_drops.loot(), "true_loot": bingo.randomize_drops.true_loot(),
                              "all_pally": bingo.randomize_drops.all_pally(),
                              "top_tier": bingo.randomize_drops.top_tiers(),
                              "steve": True, "poverty": bingo.randomize_drops.poverty(),
                              "Loot": bingo.randomize_drops.loot(), "True Loot": bingo.randomize_drops.true_loot(),
                              "STEVE": True, "Poverty": bingo.randomize_drops.poverty()}
                try:
                    run_local.local_wc(flagstring, dev)
                except subprocess.CalledProcessError:
                    try_no = 0
                    while try_no < 6:
                        try:
                            run_local.local_wc(flagstring, dev)
                            break
                        except subprocess.CalledProcessError:
                            pass
                            try_no += 1
                    else:
                        return await message.channel.send(f"Oops, I hit an error - probably a bad flagset!")
                for x in args:
                    if x.strip().casefold() == "tunes":
                        run_local.local_jdm()
                        mtype += f'_tunes'
                        jdm_spoiler = True
                    if x.strip() in ("ctunes", "Chaotic Tunes"):
                        run_local.local_jdc()
                        mtype += f'_ctunes'
                        jdm_spoiler = True
                    if x.strip() in ("notunes", "No Tunes"):
                        run_local.local_jdsilent()
                        mtype += f'_notunes'
                        jdm_spoiler = True
                for x in args:
                    if x.strip() not in local_args.keys():
                        pass
                    if x.strip().casefold() == "steve":
                        bingo.steve.steveify()
                        mtype += "_steve"
                    if x.strip().casefold() in (
                            "loot", "true_loot", "all_pally", "top_tier", "poverty") or x.strip() == "True Loot":
                        bingo.randomize_drops.run_item_rando(local_args[x.strip()])
                        mtype += f'_{x.strip()}'
                try:
                    filename = mtype + '_' + functions.generate_file_name()
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
                        await message.channel.send(
                            f"Here\'s your preset seed - {silly}\n**Preset Name**: {preset_dict[preset]['name']}\n**Created By**:"
                            f" {preset_dict[preset]['creator']}\n**Description**:"
                            f" {preset_dict[preset]['description']}",
                            file=discord.File(directory + 'seedbot.zip', filename=zipfilename),
                            view=views.ReRollView(message))
                    else:
                        await message.channel.send(f"Here's your {mtype} seed - {silly}",
                                                   file=discord.File(directory + 'seedbot.zip', filename=zipfilename),
                                                   view=views.ReRollView(message))
                except AttributeError:
                    await message.channel.send("There was a problem generating this seed - please try again!")
            except subprocess.CalledProcessError:
                return await message.channel.send(f'It looks like the randomizer didn\'t like your flags. Double-check '
                                                  f'them and try again!')
    elif roll_type == "online":
        try:
            share_url = functions.generate_v1_seed(flagstring, seed_desc, dev)['url']
            await message.channel.send(f"Here's your {mtype} seed - {silly}\n"
                                       f"> <{share_url}>", view=views.ReRollView(message))
        except TypeError:
            logging.info(f'Flagstring Error!\nSeed Type: {mtype}\nFlags:{flagstring}')
            return await message.channel.send(f'It looks like the randomizer didn\'t like your flags. Double-check '
                                              f'them and try again!')

    # Let's move on to the locally rolled stuff
    else:
        local_args = {"loot": bingo.randomize_drops.loot(), "true_loot": bingo.randomize_drops.true_loot(),
                      "all_pally": bingo.randomize_drops.all_pally(),
                      "top_tier": bingo.randomize_drops.top_tiers(),
                      "steve": True, "poverty": bingo.randomize_drops.poverty(),
                      "Loot": bingo.randomize_drops.loot(), "True Loot": bingo.randomize_drops.true_loot(),
                      "STEVE": True, "Poverty": bingo.randomize_drops.poverty()}
        try:
            run_local.local_wc(flagstring, dev)
        except subprocess.CalledProcessError:
            return await message.channel.send(f"Oops, I hit an error - probably a bad flagset!")
        for x in args:
            if x.strip().casefold() == "tunes":
                run_local.local_jdm()
                mtype += f'_tunes'
                jdm_spoiler = True
            if x.strip() in ("ctunes", "Chaotic Tunes"):
                run_local.local_jdc()
                mtype += f'_ctunes'
                jdm_spoiler = True
            if x.strip() in ("notunes", "No Tunes"):
                run_local.local_jdsilent()
                mtype += f'_notunes'
                jdm_spoiler = True
        for x in args:
            if x.strip() not in local_args.keys():
                pass
            if x.strip().casefold() == "steve":
                bingo.steve.steveify()
                mtype += "_steve"
            if x.strip() == "True Loot":
                x = "true_loot"
            if x.strip().casefold() in (
                    "loot", "true_loot", "all_pally", "top_tier", "poverty"):
                bingo.randomize_drops.run_item_rando(local_args[x.strip().lower()])
                mtype += f'_{x.strip()}'
        try:
            filename = mtype + '_' + functions.generate_file_name()
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
                await message.channel.send(
                    f"Here\'s your preset seed - {silly}\n**Preset Name**: {preset_dict[preset]['name']}\n**Created By**:"
                    f" {preset_dict[preset]['creator']}\n**Description**:"
                    f" {preset_dict[preset]['description']}",
                    file=discord.File(directory + 'seedbot.zip', filename=zipfilename),
                    view=views.ReRollView(message))
            else:
                await message.channel.send(f"Here's your {mtype} seed - {silly}",
                                           file=discord.File(directory + 'seedbot.zip', filename=zipfilename),
                                           view=views.ReRollView(message))
        except AttributeError:
            await message.channel.send("There was a problem generating this seed - please try again!")

    # After all that is done, let's add this seed to the metrics file for reporting later
    if "paint" in mtype.casefold():
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

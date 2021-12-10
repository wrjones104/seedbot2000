import discord
import os
import datetime
from maths import get_cr


import flags
from dotenv import load_dotenv
from create import generate_random_seed, generate_cr_seed, generate_hard_chaos_seed, generate_easy_chaos_seed
from custom_sprites_portraits import spraypaint


load_dotenv()

client = discord.Client()


def update_metrics(user, setting, server, url):
    f = open("db/metrics.txt", "a")
    writemsg = ''.join([str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")), ": ", user, " requested a ",
                        setting, " seed @ ", server, ". --- ", url, "\n"])
    f.write(writemsg)
    f.close()

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
            await message.channel.send(seed['flags'])
            await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

        update_metrics(str(message.author), mtype, str(message.channel), seed['share_url'])

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
            await message.channel.send(seed['flags'])
            await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

        update_metrics(str(message.author), "chaos", str(message.channel), seed['share_url'])

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
            await message.channel.send(seed['flags'])
            await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

        update_metrics(str(message.author), "truechaos", str(message.channel), seed['share_url'])

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
            await message.channel.send(r['flags'])
            await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

        update_metrics(str(message.author), "hardchaos", str(message.channel), r['share_url'])

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
            await message.channel.send(r['flags'])
            await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')

        update_metrics(str(message.author), "easychaos", str(message.channel), r['share_url'])

    if message.content.startswith('!cr') or message.content.startswith('!rated'):
        try:
            c_rating = message.content.split(" ")[1:2]
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

            except KeyError:
                await message.channel.send("BZZZZZT!!!")
                await message.channel.send("Oops, there was an flagstring error. Please send this to Jones:")
                await message.channel.send(r['flags'])
                await message.channel.send('------- FLAGS ABOVE FOR DEBUGGING -------')
        except IndexError:
            await message.channel.send("There was an error - did you include your challenge rating number?")

        type_w_rate = ''.join(["rated (", str(c_rating[0]), " > ", str(m), ")"])
        update_metrics(str(message.author), type_w_rate, str(message.channel), r['share_url'])

    if message.content.startswith("!getmetrics"):
        if message.author.id == 197757429948219392:
            with open("db/metrics.txt") as f:
                m_msg = f.read()
                f.close()
                await message.channel.send(m_msg)
        else:
            await message.channel.send("Wait a second... you're not Jones!")

    if message.content.startswith("!rateflags"):
        f2r = ' '.join(args)
        # print(f2r)
        f2rr = get_cr(f2r)[1]
        try:
            ratemsg = ' '.join([str(message.author.name), "requested a **!rateflags**. The challenge rating for this flagset is:", str(f2rr)])
            await message.channel.send(ratemsg)
            await message.delete()
        except KeyError:
            await message.channel.send("There's a problem with these flags, try again!")



    # if message.content.startswith("!test"):
    #     with open("db/test.txt") as f:
    #         test_msg = f.read()
    #         f.close()
    #         await message.channel.send(test_msg)



client.run(os.getenv('DISCORD_TOKEN'))

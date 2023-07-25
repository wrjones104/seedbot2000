import discord


async def preset_help(ctx):
    embed = discord.Embed()
    embed.title = "Preset Help"
    embed.description = open('db/presethelp.txt').read()
    return await ctx.response.send_message(embed=embed, ephemeral=True)


async def gen_help(ctx):
    embed = discord.Embed()
    embed.title = "General Help"
    embed.description = open('db/seedhelp.txt').read()
    return await ctx.response.send_message(embed=embed, ephemeral=True)


async def dev_help(ctx):
    return await ctx.response.send_message(f"--------------------------------------------\n**All dev functionality is "
                                    f"still being developed and tested.** The dev branch is located here: "
                                    f"<https://github.com/ff6wc/WorldsCollide/tree/dev>\n\nHave fun with these "
                                    f"settings, "
                                    f"but please remember:\n1. Some settings may not make it into an official "
                                    f"release\n2. Bugs are expected - please report them in the #bug-reports "
                                    f"channel (just make sure to let us know they were from a dev seed)\n3. "
                                    f"These settings may update frequently, so please check the **!devhelp** "
                                    f"often!\n--------------------------------------------\n\nUse !devseed <flags> to "
                                    f"roll a dev flagset. Alternatively, can also add the &dev argument to any "
                                    f"existing command or preset!\n\n --------------------------------------------",
                                    ephemeral=True)

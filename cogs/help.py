import discord

from discord.ext import commands
from functions import get_user


class help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="seedhelp", description="Get info on SeedBot's main commands"
    )
    async def seedhelp(self, ctx):
        seedhelp = open("db/seedhelp.txt").read()
        embed = discord.Embed()
        embed.title = "SeedBot Help"
        embed.description = seedhelp
        return await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="presethelp", description="Get info on presets")
    async def presethelp(self, ctx):
        embed = discord.Embed()
        embed.title = "Preset Help"
        embed.description = open("db/presethelp.txt").read()
        return await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(
        name="pinhelp",
        description="Pin helpful information about SeedBot in the current channel",
    )
    async def pinhelp(self, ctx):
        user = await get_user(ctx.author.id)
        try:
            if user and user[1] == 1:
                seedhelp = open("db/seedhelp.txt").read()
                embed = discord.Embed()
                embed.title = "SeedBot Help"
                embed.description = seedhelp
                helpmsg = await ctx.send(embed=embed)
                return await helpmsg.pin()
            else:
                return await ctx.send("Only Bot Admins can use this command!")
        except AttributeError:
            return await ctx.send("This command cannot be used in DMs.")


async def setup(bot):
    await bot.add_cog(help(bot))

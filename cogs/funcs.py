import git
import re
import functions

from discord.ext import commands


class funcs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="mainpull", description="Update the main WC submodule"
    )
    async def mainpull(self, ctx):
        try:
            if "Racebot Admin" in str(ctx.author.roles):
                g = git.cmd.Git("WorldsCollide/")
                g.switch("main")
                output = g.pull()
                return await ctx.send(f"Git message: {output}")
            else:
                return await ctx.send("Sorry, only bot admins can use this command!")
        except git.exc.GitError as e:
            return await ctx.send(f"Something went wrong:\n{e}")

    @commands.hybrid_command(
        name="devpull", aliases=["betapull"], description="Update the Dev submodule"
    )
    async def devpull(self, ctx):
        try:
            if "Racebot Admin" in str(ctx.author.roles):
                g = git.cmd.Git("WorldsCollide_dev/")
                g.switch("dev")
                output = g.pull()
                return await ctx.send(f"Git message: {output}")
            else:
                return await ctx.send("Sorry, only bot admins can use this command!")
        except git.exc.GitError as e:
            return await ctx.send(f"Something went wrong:\n{e}")

    @commands.hybrid_command(
        name="doorpull", description="Update the Door Rando submodule"
    )
    async def doorpull(self, ctx):
        try:
            if "Racebot Admin" in str(ctx.author.roles):
                g = git.cmd.Git("WorldsCollide_Door_Rando/")
                g.switch("doorRandomizer")
                output = g.pull()
                return await ctx.send(f"Git message: {output}")
            else:
                return await ctx.send("Sorry, only bot admins can use this command!")
        except git.exc.GitError as e:
            return await ctx.send(f"Something went wrong:\n{e}")

    @commands.hybrid_command(
        name="version", description="Get version information for Worlds Collide"
    )
    async def version(self, ctx):
        newsite = await functions.get_vers()
        with open("WorldsCollide/version.py") as x:
            smain = re.findall('"([^"]*)"', x.readlines()[0])[0]
        with open("WorldsCollide_dev/version.py") as x:
            sdev = re.findall('"([^"]*)"', x.readlines()[0])[0]
        with open("WorldsCollide_Door_Rando/version.py") as x:
            doorv = re.findall('"([^"]*)"', x.readlines()[0])[0]
        await ctx.send(
            f"**ff6worldscollide.com:** {newsite['version']}\n**SeedBot Main:** {smain}\n**SeedBot Dev:** {sdev}\n**SeedBot Door Rando:** {doorv}"
        )


async def setup(bot):
    await bot.add_cog(funcs(bot))

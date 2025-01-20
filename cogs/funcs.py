import git
import re
import functions

from discord.ext import commands
from discord.ui import Modal, TextInput
from discord import Interaction, TextStyle, app_commands

class NewUserModal(Modal):
    userid = TextInput(
        label="Enter the user's Discord ID",
        style=TextStyle.short,
    )

    botadmin = TextInput(
        label="Bot Admin?",
        style=TextStyle.short,
        default=0,
        placeholder="1 for True, 0 for False",
        max_length=1
    )

    gituser = TextInput(
        label="Git User?",
        style=TextStyle.paragraph,
        default=0,
        placeholder="1 for True, 0 for False",
        max_length=1
    )

    raceadmin = TextInput(
        label="Race Admin?",
        style=TextStyle.paragraph,
        default=0,
        placeholder="1 for True, 0 for False",
        max_length=1
    )

    def __init__(self, title: str) -> None:
        super().__init__(title=title, timeout=None)

    async def on_submit(self, interaction: Interaction, /) -> None:
        await interaction.response.defer()

class DelUserModal(Modal):
    userid = TextInput(
        label="Enter the user's Discord ID",
        style=TextStyle.short,
    )

    def __init__(self, title: str) -> None:
        super().__init__(title=title, timeout=None)

    async def on_submit(self, interaction: Interaction, /) -> None:
        await interaction.response.defer()


class funcs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="adduser", description="Add a user to SeedBot's database")
    async def adduser(self, ctx):
        user = await functions.get_user(ctx.user.id)
        if user and user[1] == 1:
            modal = NewUserModal("Add a user to SeedBot's database")
            await ctx.response.send_modal(modal)
            await modal.wait()
            await functions.add_user(str(modal.userid), str(modal.botadmin), str(modal.gituser), str(modal.raceadmin))
            return await ctx.followup.send("User successfully added!", ephemeral=True)
        else:
            return await ctx.response.send_message("Sorry, only Bot Admins can use this command!", ephemeral=True)

    @app_commands.command(name="deleteuser", description="Delete a user from SeedBot's database")
    async def deleteuser(self, ctx):
        user = await functions.get_user(ctx.user.id)
        if user and user[1] == 1:
            modal = DelUserModal("Delete a user from SeedBot's database")
            await ctx.response.send_modal(modal)
            await modal.wait()
            if str(modal.userid) == str(ctx.user.id):
                return await ctx.followup.send("Probably a bad idea to delete yourself...", ephemeral=True)
            else:
                await functions.del_user(str(modal.userid))
                return await ctx.followup.send("User successfully deleted!", ephemeral=True)
        else:
            return await ctx.response.send_message("Sorry, only Bot Admins can use this command!", ephemeral=True)

    @commands.hybrid_command(
        name="mainpull", description="Update the main WC submodule"
    )
    async def mainpull(self, ctx):
        user = await functions.get_user(ctx.author.id)
        try:
            if user and user[2] == 1:
                g = git.cmd.Git("WorldsCollide/")
                g.switch("main")
                output = g.pull()
                return await ctx.send(f"Git message: {output}")
            else:
                return await ctx.send("Sorry, only Git Users can use this command!", ephemeral=True)
        except git.exc.GitError as e:
            return await ctx.send(f"Something went wrong:\n{e}")

    @commands.hybrid_command(
        name="devpull", aliases=["betapull"], description="Update the Dev submodule"
    )
    async def devpull(self, ctx):
        user = await functions.get_user(ctx.author.id)
        try:
            if user and user[2] == 1:
                g = git.cmd.Git("WorldsCollide_dev/")
                g.switch("dev")
                output = g.pull()
                return await ctx.send(f"Git message: {output}")
            else:
                return await ctx.send("Sorry, only Git Users can use this command!", ephemeral=True)
        except git.exc.GitError as e:
            return await ctx.send(f"Something went wrong:\n{e}")

    @commands.hybrid_command(
        name="doorpull", description="Update the Door Rando submodule"
    )
    async def doorpull(self, ctx):
        user = await functions.get_user(ctx.author.id)
        try:
            if user and user[2] == 1:
                g = git.cmd.Git("WorldsCollide_Door_Rando/")
                g.switch("doorRandomizer-new")
                output = g.pull()
                return await ctx.send(f"Git message: {output}")
            else:
                return await ctx.send("Sorry, only Git Users can use this command!", ephemeral=True)
        except git.exc.GitError as e:
            return await ctx.send(f"Something went wrong:\n{e}")

    @commands.hybrid_command(
        name="practicepull", description="Update the FF6WC Practice submodule"
    )
    async def practicepull(self, ctx):
        user = await functions.get_user(ctx.author.id)
        try:
            if user and user[2] == 1:
                g = git.cmd.Git("WorldsCollide_practice/")
                g.switch("kpractice")
                output = g.pull()
                return await ctx.send(f"Git message: {output}")
            else:
                return await ctx.send("Sorry, only Git Users can use this command!", ephemeral=True)
        except git.exc.GitError as e:
            return await ctx.send(f"Something went wrong:\n{e}")

    @commands.hybrid_command(
        name="lgpull", description="Update the FF6WC Location_Gating submodule"
    )
    async def lgpull(self, ctx):
        user = await functions.get_user(ctx.author.id)
        try:
            if user and user[2] == 1:
                g = git.cmd.Git("WorldsCollide_location_gating1/")
                g.switch("loc-gated")
                output = g.pull()
                return await ctx.send(f"Git message: {output}")
            else:
                return await ctx.send("Sorry, only Git Users can use this command!", ephemeral=True)
        except git.exc.GitError as e:
            return await ctx.send(f"Something went wrong:\n{e}")

    @commands.hybrid_command(
        name="worldshufflepull", description="Update the FF6WC Shuffle by World submodule"
    )
    async def worldshufflepull(self, ctx):
        user = await functions.get_user(ctx.author.id)
        try:
            if user and user[2] == 1:
                g = git.cmd.Git("WorldsCollide_shuffle_by_world/")
                g.switch("chest-shop-suffle-by-world")
                output = g.pull()
                return await ctx.send(f"Git message: {output}")
            else:
                return await ctx.send("Sorry, only Git Users can use this command!", ephemeral=True)
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

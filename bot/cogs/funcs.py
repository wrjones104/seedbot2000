import git
import re
from bot import functions

from discord.ext import commands
from discord.ui import Modal, TextInput
from discord import Interaction, TextStyle, app_commands
from django.conf import settings
from webapp.models import UserPermission

def get_submodule_path(name: str):
    """Constructs the absolute path to a submodule directory."""
    return settings.BASE_DIR / "randomizer_forks" / name

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

    async def _git_pull_command(self, ctx, submodule_name: str, branch_name: str):
        try:
            # Use the Django ORM for a cleaner permission check.
            user_perms = await UserPermission.objects.aget(user_id=ctx.author.id)
            if not user_perms.git_user:
                return await ctx.send("Sorry, only Git Users can use this command!", ephemeral=True)

            # Use the new helper to get the correct path
            repo_path = get_submodule_path(submodule_name)
            
            g = git.cmd.Git(repo_path)
            g.switch(branch_name)
            output = g.pull()
            await ctx.send(f"Git message for `{submodule_name}`:\n```{output}```")

        except UserPermission.DoesNotExist:
            await ctx.send("Sorry, you do not have permissions for this command!", ephemeral=True)
        except git.exc.GitError as e:
            await ctx.send(f"An error occurred with Git:\n```{e}```")

    @app_commands.command(name="adduser", description="Add or update a user in SeedBot's database")
    async def adduser(self, ctx: Interaction):
        try:
            # Check permissions using the ORM
            user_perms = await UserPermission.objects.aget(user_id=ctx.user.id)
            if not user_perms.bot_admin:
                return await ctx.response.send_message("Sorry, only Bot Admins can use this command!", ephemeral=True)
        except UserPermission.DoesNotExist:
            return await ctx.response.send_message("Sorry, only Bot Admins can use this command!", ephemeral=True)

        modal = NewUserModal("Add/Update User")
        await ctx.response.send_modal(modal)
        await modal.wait()

        try:
            # Use the ORM to create or update the user, which is safer.
            await UserPermission.objects.acreate(
                user_id=int(str(modal.userid)),
                bot_admin=int(str(modal.botadmin)),
                git_user=int(str(modal.gituser)),
                race_admin=int(str(modal.raceadmin))
            )
            await ctx.followup.send(f"User `{modal.userid}` has been added/updated.", ephemeral=True)
        except (ValueError, TypeError):
            await ctx.followup.send("Invalid input. Please ensure User ID and permissions are numbers (1 or 0).", ephemeral=True)
        except Exception as e:
            await ctx.followup.send(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="deleteuser", description="Delete a user from SeedBot's database")
    async def deleteuser(self, ctx: Interaction):
        try:
            # Check permissions using the ORM
            user_perms = await UserPermission.objects.aget(user_id=ctx.user.id)
            if not user_perms.bot_admin:
                return await ctx.response.send_message("Sorry, only Bot Admins can use this command!", ephemeral=True)
        except UserPermission.DoesNotExist:
            return await ctx.response.send_message("Sorry, only Bot Admins can use this command!", ephemeral=True)

        modal = DelUserModal("Delete User")
        await ctx.response.send_modal(modal)
        await modal.wait()

        target_userid_str = str(modal.userid)
        if not target_userid_str.isdigit():
            return await ctx.followup.send("Invalid User ID.", ephemeral=True)
        
        target_userid = int(target_userid_str)
        if target_userid == ctx.user.id:
            return await ctx.followup.send("You cannot delete yourself.", ephemeral=True)

        try:
            # Use the ORM to find and delete the user
            user_to_delete = await UserPermission.objects.aget(user_id=target_userid)
            await user_to_delete.adelete()
            await ctx.followup.send(f"User `{target_userid}` has been deleted.", ephemeral=True)
        except UserPermission.DoesNotExist:
            await ctx.followup.send(f"User `{target_userid}` not found in the database.", ephemeral=True)
        except Exception as e:
            await ctx.followup.send(f"An error occurred: {e}", ephemeral=True)

    @commands.hybrid_command(name="mainpull", description="Update the main WC submodule")
    async def mainpull(self, ctx: commands.Context):
        await self._git_pull_command(ctx, "WorldsCollide", "main")

    @commands.hybrid_command(name="devpull", aliases=["betapull"], description="Update the Dev submodule")
    async def devpull(self, ctx: commands.Context):
        await self._git_pull_command(ctx, "WorldsCollide_dev", "dev")

    @commands.hybrid_command(name="doorpull", description="Update the Door Rando submodule")
    async def doorpull(self, ctx: commands.Context):
        await self._git_pull_command(ctx, "WorldsCollide_Door_Rando", "doorRandomizer-new")

    @commands.hybrid_command(name="practicepull", description="Update the FF6WC Practice submodule")
    async def practicepull(self, ctx: commands.Context):
        await self._git_pull_command(ctx, "WorldsCollide_practice", "kpractice")

    @commands.hybrid_command(name="lgpull", description="Update the FF6WC Location_Gating submodule")
    async def lgpull(self, ctx: commands.Context):
        await self._git_pull_command(ctx, "WorldsCollide_location_gating1", "loc-gated")

    @commands.hybrid_command(name="worldshufflepull", description="Update the FF6WC Shuffle by World submodule")
    async def worldshufflepull(self, ctx: commands.Context):
        await self._git_pull_command(ctx, "WorldsCollide_shuffle_by_world", "worlds-divided")

    @commands.hybrid_command(name="version", description="Get version information for Worlds Collide")
    async def version(self, ctx: commands.Context):
        versions = {}
        submodules_to_check = {
            "SeedBot Main": "WorldsCollide",
            "SeedBot Dev": "WorldsCollide_dev",
            "SeedBot Door Rando": "WorldsCollide_Door_Rando",
        }

        for name, path in submodules_to_check.items():
            try:
                # Use the new helper to get the correct path
                version_file = get_submodule_path(path) / "version.py"
                with open(version_file, "r") as f:
                    # Use a safer regex to find the version string
                    match = re.search(r'version = "([^"]+)"', f.read())
                    if match:
                        versions[name] = match.group(1)
                    else:
                        versions[name] = "Not found"
            except FileNotFoundError:
                versions[name] = "Not found"
        
        # This part is unchanged as it hits the live API
        newsite = await functions.get_vers()
        
        # Build the response string
        response_lines = [f"**ff6worldscollide.com:** {newsite['version']}"]
        for name, ver in versions.items():
            response_lines.append(f"**{name}:** {ver}")
            
        await ctx.send("\n".join(response_lines))



async def setup(bot):
    await bot.add_cog(funcs(bot))

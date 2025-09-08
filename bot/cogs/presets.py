import discord
import datetime
from discord.ext import commands
from django.urls import reverse
from django.conf import settings
from webapp.models import Preset

# --- UI Components for Preset Management ---

class DeleteConfirmationView(discord.ui.View):
    """A view that asks for confirmation before deleting a preset."""
    def __init__(self, preset_to_delete, original_author_id):
        super().__init__(timeout=60)
        self.preset_to_delete = preset_to_delete
        self.original_author_id = original_author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Ensure only the original command author can interact with this view.
        if interaction.user.id != self.original_author_id:
            await interaction.response.send_message("You are not authorized to perform this action.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Confirm Delete", style=discord.ButtonStyle.danger)
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        preset_name = self.preset_to_delete.preset_name
        await self.preset_to_delete.adelete()
        await interaction.response.edit_message(content=f"✅ The preset '{preset_name}' has been deleted.", view=None)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Deletion cancelled.", view=None)
        self.stop()

    async def on_timeout(self):
        # Disable buttons and notify the user when the view times out.
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(content="Deletion confirmation timed out.", view=self)

class ManagePresetView(discord.ui.View):
    """A view with buttons to Roll or Delete a preset."""
    def __init__(self, preset, original_author_id):
        super().__init__(timeout=300)
        self.preset = preset
        self.original_author_id = original_author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.original_author_id:
            await interaction.response.send_message("You are not authorized to perform this action.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Roll", style=discord.ButtonStyle.primary)
    async def roll_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from bot.cogs.seedgen import handle_interaction_roll # Local import to avoid circular dependency issues
        
        await interaction.response.defer(thinking=True, ephemeral=True)
        
        # We need to construct a 'button_info' tuple to pass to the handler
        button_info = (
            None, # view_id
            "Roll", # button_name
            f"manage_roll_{self.preset.pk}", # button_id
            self.preset.flags,
            self.preset.arguments,
            True, # is_preset
            f"preset_{self.preset.pk.replace(' ', '_')}" # mtype
        )
        await handle_interaction_roll(interaction, button_info)
        
        # Disable the button after it's been clicked to prevent multiple rolls
        button.disabled = True
        await interaction.edit_original_response(view=self)

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = DeleteConfirmationView(self.preset, self.original_author_id)
        await interaction.response.send_message(
            f"Are you sure you want to permanently delete the preset '{self.preset.preset_name}'?", 
            view=view, 
            ephemeral=True
        )
        # Disable this view's buttons after opening the confirmation
        self.stop()
        for item in self.children:
            item.disabled = True
        await interaction.edit_original_response(view=self)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=self)

# --- Main Cog ---

class PresetCog(commands.Cog, name="Presets"):
    """Commands for creating and managing presets."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(self, ctx: commands.Context, error: Exception):
        """Handles errors for commands in this cog."""
        await ctx.send(f"An error occurred in the Preset command: {error}", ephemeral=True)

    @commands.hybrid_command(name="addpreset", description="Add a new preset.")
    async def add_preset(self, ctx: commands.Context, name: str, flags: str, description: str = "", arguments: str = "", hidden: bool = False):
        """Creates a new preset. Arguments should be a space-separated string."""
        try:
            await Preset.objects.acreate(
                preset_name=name,
                creator_id=ctx.author.id,
                creator_name=ctx.author.display_name,
                created_at=str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")),
                flags=flags,
                description=description,
                arguments=arguments,
                official=False, # Official status can only be set via Django Admin now
                hidden=hidden,
                gen_count=0
            )
            website_url = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else "your-website.com"
            view_url = f"https://{website_url}{reverse('preset-detail', args=[name])}"

            embed = discord.Embed(
                title="✅ Preset Saved!",
                description=f"Your preset '{name}' has been saved successfully.",
                color=discord.Color.green()
            )
            view = discord.ui.View()
            view.add_item(discord.ui.Button(label="View on Website", url=view_url))
            
            await ctx.send(embed=embed, view=view)

        except Exception:
            await ctx.send(f"Could not save preset. A preset with the name '{name}' may already exist.", ephemeral=True)

    @commands.hybrid_command(name="deletepreset", description="Deletes one of your presets.")
    async def delete_preset(self, ctx: commands.Context, name: str):
        """Initiates the safe deletion process for a preset."""
        try:
            preset = await Preset.objects.aget(preset_name__iexact=name)
            if preset.creator_id != ctx.author.id:
                return await ctx.send("You can only delete presets that you created.", ephemeral=True)
            
            view = DeleteConfirmationView(preset, ctx.author.id)
            await ctx.send(f"Are you sure you want to permanently delete the preset '{preset.preset_name}'?", view=view, ephemeral=True)

        except Preset.DoesNotExist:
            await ctx.send(f"I couldn't find a preset with that name!", ephemeral=True)

    @commands.hybrid_command(name="managepreset", description="Manage one of your presets.")
    async def manage_preset(self, ctx: commands.Context, name: str):
        """Shows details and management options for a preset."""
        try:
            preset = await Preset.objects.aget(preset_name__iexact=name)
            
            embed = discord.Embed(title=f"Managing Preset: '{preset.preset_name}'")
            embed.description = preset.description or "No description provided."
            if preset.arguments:
                embed.add_field(name="Arguments", value=f"`{preset.arguments}`", inline=False)
            embed.set_footer(text=f"Created by: {preset.creator_name}")

            view = ManagePresetView(preset, ctx.author.id)
            website_url = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else "your-website.com"
            edit_url = f"https://{website_url}{reverse('preset-update', args=[preset.pk])}"
            view.add_item(discord.ui.Button(label="Edit on Website", style=discord.ButtonStyle.link, url=edit_url))

            await ctx.send(embed=embed, view=view)

        except Preset.DoesNotExist:
            await ctx.send(f"I couldn't find a preset with that name!", ephemeral=True)

    @commands.hybrid_command(name="mypresets", description="Links to your personal preset page.")
    async def my_presets(self, ctx: commands.Context):
        """Provides a link to your user profile on the SeedBot website."""
        website_url = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else "your-website.com"
        profile_url = f"https://{website_url}{reverse('my-profile')}"
        
        embed = discord.Embed(
            title=f"📁 Your Presets",
            description="You can view, create, and manage all of your presets on your personal profile page.",
            color=discord.Color.blue()
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Go to My Profile", url=profile_url))
        await ctx.send(embed=embed, view=view)

    @commands.hybrid_command(name="allpresets", description="Links to the main preset list.")
    async def all_presets(self, ctx: commands.Context):
        """Provides a link to the full list of presets on the SeedBot website."""
        website_url = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else "your-website.com"
        list_url = f"https://{website_url}{reverse('preset-list')}"
        
        embed = discord.Embed(
            title="📖 All Presets",
            description="Browse, search, and sort the full list of community presets on the website.",
            color=discord.Color.blue()
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Go to Preset List", url=list_url))
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(PresetCog(bot))
from typing import Optional
import io
import discord
import datetime
from discord.ext import commands
from django.urls import reverse
from django.conf import settings
from webapp.models import UserPermission
from bot.utils.firestore_client import db_async, sanitize_preset_name, get_base_url, FirestorePresetAdapter

from bot.constants import DEFAULT_TIMEOUT, SHORT_TIMEOUT, WEBSITE_URL

class DeleteConfirmationView(discord.ui.View):
    """A view that asks for confirmation before deleting a preset."""
    def __init__(self, doc_id, preset_name, original_author_id):
        super().__init__(timeout=60)
        self.doc_id = doc_id
        self.preset_name = preset_name
        self.original_author_id = original_author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.original_author_id:
            await interaction.response.send_message("You are not authorized to perform this action.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Confirm Delete", style=discord.ButtonStyle.danger)
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await db_async.collection("presets").document(self.doc_id).delete()
        await interaction.response.edit_message(content=f"✅ The preset '{self.preset_name}' has been deleted.", view=None)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Deletion cancelled.", view=None)
        self.stop()

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(content="Deletion confirmation timed out.", view=self)

class ManagePresetView(discord.ui.View):
    """A view with buttons to Roll or Delete a preset."""
    def __init__(self, doc_id, preset_name, preset_flags, preset_arguments, original_author_id):
        super().__init__(timeout=300)
        self.doc_id = doc_id
        self.preset_name = preset_name
        self.preset_flags = preset_flags
        self.preset_arguments = preset_arguments
        self.original_author_id = original_author_id
        self.message: Optional[discord.Message] = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.original_author_id:
            await interaction.response.send_message("You are not authorized to perform this action.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Roll", style=discord.ButtonStyle.primary)
    async def roll_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from bot.cogs.seedgen import handle_interaction_roll # Local import to avoid circular dependency issues
        
        await interaction.response.defer(thinking=True, ephemeral=True)
        
        button_info = (
            None, # view_id
            "Roll", # button_name
            f"manage_roll_{self.doc_id}", # button_id
            self.preset_flags,
            self.preset_arguments,
            True, # is_preset
            f"preset_{self.doc_id.replace(' ', '_')}" # mtype
        )
        await handle_interaction_roll(interaction, button_info)
        
        # Disable the button after it's been clicked to prevent multiple rolls
        button.disabled = True
        await interaction.edit_original_response(view=self)

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = DeleteConfirmationView(self.doc_id, self.preset_name, self.original_author_id)
        await interaction.response.send_message(
            f"Are you sure you want to permanently delete the preset '{self.preset_name}'?", 
            view=view, 
            ephemeral=True
        )
        # Disable this view's buttons after opening the confirmation
        self.stop()
        for item in self.children:
            item.disabled = True
        
        await interaction.edit_original_response(view=self)

        confirmation_view = DeleteConfirmationView(self.preset, self.original_author_id)
        confirmation_view.message = await interaction.followup.send(
            f"Are you sure you want to permanently delete the preset '{self.preset.preset_name}'?", 
            view=confirmation_view, 
            ephemeral=True
        )

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

    @commands.hybrid_command(name="addpreset", aliases=["savepreset"], description="Add a new preset.")
    async def add_preset(self, ctx: commands.Context, name: str, flags: str, description: str = "", arguments: str = "", hidden: bool = False):
        """Creates a new preset. Arguments should be a space-separated string."""
        try:
            base_sanitized = sanitize_preset_name(name)
            sanitized_id = base_sanitized
            counter = 1
            while True:
                preset_name_lower = sanitized_id.lower()
                query = db_async.collection("presets").where("preset_name_lower", "==", preset_name_lower).limit(1).get()
                results = await query
                if not results:
                    break
                sanitized_id = f"{base_sanitized}-{counter}"
                counter += 1

            doc_data = {
                "preset_name": sanitized_id,
                "preset_name_lower": sanitized_id.lower(),
                "creator_id": str(ctx.author.id),
                "creator_name": ctx.author.display_name,
                "created_at": datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"),
                "flags": flags,
                "description": description,
                "arguments": arguments,
                "official": bool(False), # Official status can only be set via GCP Console/Admin now
                "hidden": bool(hidden),
                "gen_count": 0
            }
            await db_async.collection("presets").document(sanitized_id).set(doc_data)

            view_url = f"{get_base_url()}{reverse('preset-detail', args=[sanitized_id])}"

            embed = discord.Embed(
                title="✅ Preset Saved!",
                description=f"Your preset '{sanitized_id}' has been saved successfully.",
                color=discord.Color.green()
            )
            view = discord.ui.View()
            view.add_item(discord.ui.Button(label="View on Website", url=view_url))
            
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            await ctx.send(f"Could not save preset. Error: {e}", ephemeral=True)

    @commands.hybrid_command(name="delpreset", aliases=["deletepreset"], description="Deletes one of your presets.")
    async def delete_preset(self, ctx: commands.Context, name: str):
        """Initiates the safe deletion process for a preset."""
        try:
            sanitized_id = sanitize_preset_name(name)
            doc_ref = db_async.collection("presets").document(sanitized_id)
            doc_snap = await doc_ref.get()
            if not doc_snap.exists:
                await ctx.send(f"I couldn't find a preset with that name!", ephemeral=True)
                return
            
            data = doc_snap.to_dict()
            creator_id = data.get("creator_id")
            
            try:
                user_perms = await UserPermission.objects.aget(user_id=ctx.author.id)
                is_admin = bool(user_perms.bot_admin)
            except UserPermission.DoesNotExist:
                is_admin = False

            if str(ctx.author.id) != str(creator_id) and not is_admin:
                return await ctx.send("You do not have permission to delete this preset. Only the creator or an admin can delete it.", ephemeral=True)
            
            view = DeleteConfirmationView(sanitized_id, data.get("preset_name"), ctx.author.id)
            await ctx.send(f"Are you sure you want to permanently delete the preset '{data.get('preset_name')}'?", view=view, ephemeral=True)

        except Exception as e:
            await ctx.send(f"An error occurred while trying to delete the preset: {e}", ephemeral=True)

    @commands.hybrid_command(name="managepreset", description="Manage one of your presets.")
    async def manage_preset(self, ctx: commands.Context, name: str):
        """Shows details and management options for a preset."""
        try:
            sanitized_id = sanitize_preset_name(name)
            doc_snap = await db_async.collection("presets").document(sanitized_id).get()
            if not doc_snap.exists:
                await ctx.send(f"I couldn't find a preset with that name!", ephemeral=True)
                return
            
            data = doc_snap.to_dict()
            embed = discord.Embed(title=f"Managing Preset: '{data.get('preset_name')}'")
            embed.description = data.get("description") or "No description provided."
            if data.get("arguments"):
                embed.add_field(name="Arguments", value=f"`{data.get('arguments')}`", inline=False)
            embed.set_footer(text=f"Created by: {data.get('creator_name')}")

            view = ManagePresetView(
                doc_id=sanitized_id,
                preset_name=data.get("preset_name"),
                preset_flags=data.get("flags", ""),
                preset_arguments=data.get("arguments", ""),
                original_author_id=ctx.author.id
            )
            edit_url = f"{get_base_url()}{reverse('preset-update', args=[sanitized_id])}"
            view.add_item(discord.ui.Button(label="Edit on Website", style=discord.ButtonStyle.link, url=edit_url))

            view.message = await ctx.send(embed=embed, view=view)

        except Exception as e:
            await ctx.send(f"An error occurred while managing the preset: {e}", ephemeral=True)

    @commands.hybrid_command(name="mypresets", description="Links to your personal preset page.")
    async def my_presets(self, ctx: commands.Context):
        """Provides a link to your user profile on the SeedBot website."""
        profile_url = f"{get_base_url()}{reverse('my-profile')}"
        
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
        list_url = f"{get_base_url()}{reverse('preset-list')}"
        
        embed = discord.Embed(
            title="📖 All Presets",
            description="Browse, search, and sort the full list of community presets on the website.",
            color=discord.Color.blue()
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Go to Preset List", url=list_url))
        await ctx.send(embed=embed, view=view)

    @commands.hybrid_command(name="pflags", description="Shows the flags for a specific preset.")
    async def pflags(self, ctx: commands.Context, *, name: str):
        """Displays the flags for a given preset."""
        try:
            preset_name_lower = name.lower()
            query = await db_async.collection("presets").where("preset_name_lower", "==", preset_name_lower).limit(1).get()
            if not query:
                await ctx.send(f"I couldn't find a preset named '{name}'.", ephemeral=True)
                return
            preset = FirestorePresetAdapter(query[0].to_dict())

            # --- Define Limits ---
            # 1024 limit - 6 chars for ```...```
            EMBED_FIELD_LIMIT = 1018 
            # 2000 limit - 6 chars for ```...``` and ~20 for "Flags:\n"
            MESSAGE_LIMIT = 1970 

            flag_len = len(preset.flags) if preset.flags else 0
            arg_len = len(preset.arguments) if preset.arguments else 0

            # --- Case 1: Everything fits in the embed (Happy Path) ---
            if flag_len <= EMBED_FIELD_LIMIT and arg_len <= EMBED_FIELD_LIMIT:
                embed = discord.Embed(
                    title=f"🚩 Flags for '{preset.preset_name}'",
                    color=discord.Color.blue()
                )
                if preset.flags:
                    embed.add_field(name="Flags", value=f"```{preset.flags}```", inline=False)
                if preset.arguments:
                    embed.add_field(name="Arguments", value=f"```{preset.arguments}```", inline=False)
                
                await ctx.send(embed=embed)
                return # We're done

            # --- Case 2: One or more fields are too long for an embed ---
            # Send a plain title message first
            await ctx.send(f"🚩 **Flags for '{preset.preset_name}'**")

            # --- Handle Flags (3-tier logic) ---
            if preset.flags:
                if flag_len <= MESSAGE_LIMIT:
                    # Send as code block message
                    await ctx.send(f"**Flags:**\n```{preset.flags}```")
                else:
                    # Send as file
                    flag_fp = io.BytesIO(preset.flags.encode('utf-8'))
                    file = discord.File(flag_fp, filename=f"{preset.preset_name}_flags.txt")
                    await ctx.send("**Flags:** (See attached file, too long to display)", file=file)

            # --- Handle Arguments (3-tier logic) ---
            if preset.arguments:
                if arg_len <= MESSAGE_LIMIT:
                    # Send as code block message
                    await ctx.send(f"**Arguments:**\n```{preset.arguments}```")
                else:
                    # Send as file
                    arg_fp = io.BytesIO(preset.arguments.encode('utf-8'))
                    file = discord.File(arg_fp, filename=f"{preset.preset_name}_args.txt")
                    await ctx.send("**Arguments:** (See attached file, too long to display)", file=file)

        except Exception as e:
            await ctx.send(f"An error occurred while fetching the preset: {e}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(PresetCog(bot))
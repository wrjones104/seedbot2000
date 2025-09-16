import discord
from discord.ext import commands
from django.urls import reverse
from django.conf import settings
from typing import Optional

from bot.constants import DEFAULT_TIMEOUT, WEBSITE_URL


class HelpView(discord.ui.View):
    """The main view for the /help command, containing the dropdown."""
    def __init__(self, author_id):
        super().__init__(timeout=DEFAULT_TIMEOUT)
        self.author_id = author_id
        self.add_item(HelpSelect())
        self.message: Optional[discord.Message] = None
        
        website_url = WEBSITE_URL
        self.add_item(discord.ui.Button(label="Visit Website", url=website_url))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Please run the `/help` command yourself to use this menu.", ephemeral=True)
            return False
        return True
    
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=self)


class HelpSelect(discord.ui.Select):
    """The dropdown menu for selecting a help category."""
    def __init__(self):
        options = [
            discord.SelectOption(label="Seed Rolling", emoji="🎲", description="Commands like !rando and !chaos."),
            discord.SelectOption(label="Preset Management", emoji="📁", description="Commands for managing your presets."),
            discord.SelectOption(label="Seed Modifiers", emoji="✨", description="All about '&' arguments like &tunes."),
            discord.SelectOption(label="Practice Seeds", emoji="⚔️", description="Information on practice seeds."),
        ]
        super().__init__(placeholder="Select a category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        selection = self.values[0]
        embed = self.get_embed_for_category(selection)
        
        await interaction.edit_original_response(embed=embed)

    def get_embed_for_category(self, category: str) -> discord.Embed:
        """Returns the appropriate help embed based on the selected category."""
        if category == "Seed Rolling":
            embed = discord.Embed(title="🎲 Help: Seed Rolling Commands", color=discord.Color.green())
            embed.add_field(name="!rando", value="Rolls a seed with light randomization, perfect for quick runs.", inline=False)
            embed.add_field(name="!chaos", value="Rolls a wackier seed with more liberal randomization.", inline=False)
            embed.add_field(name="!truechaos", value="Randomizes everything with no weighting. A true test of skill!", inline=False)
            embed.add_field(name="!preset <name>", value="Rolls a seed from a saved preset.", inline=False)
            embed.add_field(name="!rollseed <flags>", value="Rolls a seed with a specific flagstring.", inline=False)
            embed.add_field(name="!devseed <flags>", value="Rolls a seed using a dev version of the randomizer.", inline=False)
            return embed

        if category == "Preset Management":
            embed = discord.Embed(title="📁 Help: Preset Management", color=discord.Color.blue())
            embed.description = "Managing presets is now easier on the website, but you can still use these commands."
            embed.add_field(name="/addpreset", value="Creates a new preset.", inline=False)
            embed.add_field(name="/deletepreset", value="Safely deletes one of your presets.", inline=False)
            embed.add_field(name="/managepreset", value="Shows a menu to Roll, Delete, or Edit a preset.", inline=False)
            embed.add_field(name="/mypresets", value="Links to your personal profile page on the website.", inline=False)
            embed.add_field(name="/allpresets", value="Links to the full list of community presets.", inline=False)
            embed.add_field(name="/pflags <name>", value="Quickly shows the flags for a preset in Discord.", inline=False)
            return embed

        if category == "Seed Modifiers":
            embed = discord.Embed(title="✨ Help: Seed Modifiers (Arguments)", color=discord.Color.orange())
            embed.description = "Add these to any seed command to modify the roll (e.g., `!chaos &tunes &paint`)."
            
            gfx_audio = "`&paint` / `&palette` / `&kupo`, `&tunes` / `&ctunes` / `&notunes`, `&noflashes`"
            gameplay = "`&loot`, `&emptyshops`, `&emptychests`, `&obj`, `&hundo`, `&dash`, `&yeet`, `cg`"
            forks = "`&dev`, `&lg1` / `&lg2`, `&ws` / `&csi`, `&doors` / `&dungeoncrawl` / `&doorslite` / `&doorx` / `&maps` / `&mapx`"
            utility = "`&spoilers` / `&nospoilers`, `&mystery`, `&ap` / `&apts` / `&apsafe` / `&aptssafe`, `&flagsonly`"
            
            embed.add_field(name="🎨 Graphics & Audio", value=gfx_audio, inline=False)
            embed.add_field(name="🕹️ Gameplay", value=gameplay, inline=False)
            embed.add_field(name="🍴 Alternate Forks", value=forks, inline=False)
            embed.add_field(name="🔧 Utility", value=utility, inline=False)
            return embed

        if category == "Practice Seeds":
            embed = discord.Embed(title="⚔️ Help: Practice Seeds", color=discord.Color.red())
            embed.description = "The practice ROM allows you to fight Final Kefka from the airship and any boss by talking to Gestahl. Talk to Leo to recruit characters. Use the airship NPC to swap and equip your party."
            embed.add_field(name="Command", value="`!practice` - Rolls a practice ROM instance.", inline=False)
            embed.add_field(name="More Info", value="For a detailed guide on all practice ROM options, go to https://seedbot.net/practice.", inline=False)
            return embed
        
        return discord.Embed(title="Help", description="Select a category from the dropdown to learn more.")

# --- Main Cog Class ---

class HelpCog(commands.Cog, name="Help"):
    """Provides a centralized, interactive help command."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description="Get interactive help for SeedBot commands.")
    async def help(self, ctx: commands.Context):
        """Displays the main help menu."""
        embed = discord.Embed(
            title="SeedBot Help",
            description="Welcome! I can roll seeds for Final Fantasy VI: Worlds Collide, manage presets, and more.\n\nSelect a category below to learn about my commands, or visit the website for a full list of presets.",
            color=discord.Color.purple()
        )
        view = HelpView(ctx.author.id)
        view.message = await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
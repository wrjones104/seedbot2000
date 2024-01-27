import discord
import functions
import flag_builder
from discord.ext import commands
from discord import app_commands

class seedgen(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="rando")
    async def on_message(self, ctx, *args):
        msg = await ctx.send(f"Bundling something up for {ctx.author.display_name}...")
        argparse = await functions.argparse(ctx, flag_builder.standard(), functions.splitargs(args))

    @app_commands.command(name="okay", description="dunno, mate")
    async def okay(self, interaction:discord.Interaction):
        await interaction.response.send_message("sup")



async def setup(bot):
    await bot.add_cog(seedgen(bot))

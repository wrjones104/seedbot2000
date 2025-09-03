import discord
from discord.ui import View
from discord.ext import commands
from typing import cast

from bot.functions import get_button_info
from bot.cogs.seedgen import handle_interaction_roll, SeedGen


class PersistentButton(discord.ui.Button):
    async def callback(self, interaction: discord.Interaction):
        try:
            button_info = await get_button_info(self.custom_id)
            await handle_interaction_roll(interaction, button_info)
        except Exception as e:
            # --- FIX: Use typing.cast to inform the linter of the correct type ---
            bot = cast(commands.Bot, interaction.client)
            cog: SeedGen = bot.get_cog('SeedGen')
            if cog:
                await cog.cog_command_error(interaction, e)
            else:
                if not interaction.response.is_done():
                    await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)
                else:
                    await interaction.followup.send("An unexpected error occurred.", ephemeral=True)


class ButtonView(discord.ui.View):
    def __init__(self, options_and_ids):
        super().__init__(timeout=None)
        for data_tuple in options_and_ids:
            _, option, button_id, _, _, _, _ = data_tuple
            button = PersistentButton(
                label=option, custom_id=button_id, style=discord.ButtonStyle.green
            )
            self.add_item(button)


class ReRollExtraView(View):
    def __init__(self, interaction_ctx, button_info):
        super().__init__(timeout=None)
        self.interaction_ctx = interaction_ctx
        self.button_info = button_info

    @discord.ui.select(
        min_values=1,
        max_values=15,
        placeholder="Select extra options to add to your reroll...",
        options=[
            discord.SelectOption(label="Tunes", emoji="<:maria:447221707279826944>", description="Randomize the music"),
            discord.SelectOption(label="ChaoticTunes", emoji="<:funkbaba:836700117826142229>", description="Chaotically randomize the music"),
            discord.SelectOption(label="NoTunes", emoji="<:GogoMute:667486074427146252>", description="No music, just SFX"),
            discord.SelectOption(label="Palette", emoji="<:SketchUlty:666902749987733514>", description="Randomize sprite color palettes"),
            discord.SelectOption(label="Paint", emoji="<:yikes:447221708303106048>", description="Randomize the sprites, portraits and palettes"),
            discord.SelectOption(label="Kupo", emoji="<:MogHappy:667477014801809428>", description="Everyone's a moogle!"),
            discord.SelectOption(label="FancyGau", emoji="<:gau_smoosh:956342867897516102>", description="He cleans up nice!"),
            discord.SelectOption(label="Objectives", emoji="<a:KefkaLaugh:666889733301075979>", description="Randomize the objectives of the seed"),
            discord.SelectOption(label="NoSpoilers", emoji="<:StragoNap:667477014793682944>", description="Ensure spoiler log IS NOT included"),
            discord.SelectOption(label="Spoilers", emoji="<:strago_smoosh:956342464548061245>", description="Ensure spoiler log IS included"),
            discord.SelectOption(label="NoFlashes", emoji="<:LeoShock:666915710488018946>", description='Forces the "Remove Worst Flashes" flag'),
            discord.SelectOption(label="Yeet", emoji="<:EdgarChainSaw:666886468953964566>", description='Forces the "Y-NPC Remove" flag'),
            discord.SelectOption(label="Hundo", emoji="<:ff6worGitgud:933089780382716005>", description="Forces a 100% complete seed"),
            discord.SelectOption(label="Loot", emoji="<:LockeCaught:667228085434712077>", description="All enemy drops and steals are randomized"),
            discord.SelectOption(label="Mystery", emoji="<:what:414522067648643083>", description="Hides the flags from the log and track menu"),
            discord.SelectOption(label="Zozo", emoji="<:lul:840298070439624774>", description="Shuffles characters and hides their original names"),
            discord.SelectOption(label="STEVE", emoji="<:Kappa:698619218358304868>", description="Everything is and always will be STEVE"),
        ],
        custom_id="re_roll_extra_selector",
    )
    async def extra_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        try:
            extra_args_str = " ".join(select.values)
            await handle_interaction_roll(interaction, self.button_info, extra_args=extra_args_str)
        except Exception as e:
            # --- FIX: Use typing.cast to inform the linter of the correct type ---
            bot = cast(commands.Bot, interaction.client)
            cog: SeedGen = bot.get_cog('SeedGen')
            if cog:
                await cog.cog_command_error(interaction, e)
            else:
                if not interaction.response.is_done():
                    await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)
                else:
                    await interaction.followup.send("An unexpected error occurred.", ephemeral=True)
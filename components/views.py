import discord
from discord.ui import View

from functions import get_button_info
from cogs.seedgen import roll_button_seed


class PersistentButton(discord.ui.Button):
    async def callback(self, interaction: discord.Interaction):
        button_id = self.custom_id
        button_info = await get_button_info(button_id)
        await interaction.response.send_message("Bundling something up...")
        msg = await interaction.original_response()
        return await roll_button_seed(
            interaction,
            button_info[1],
            button_info[2],
            button_info[3],
            button_info[4],
            button_info[5],
            button_info[6],
            msg,
            False,
        )


class ButtonView(discord.ui.View):
    def __init__(self, options_and_ids):
        super().__init__(timeout=None)

        for (
            view_ids,
            option,
            button_id,
            flags,
            bargs,
            ispreset,
            mtype,
        ) in options_and_ids:
            button = PersistentButton(
                label=option, custom_id=button_id, style=discord.ButtonStyle.green
            )
            self.add_item(button)


class ReRollExtraView(View):
    def __init__(
        self,
        ctx,
        button_name,
        button_id,
        button_flags,
        button_args,
        button_ispreset,
        button_mtype,
    ):
        super().__init__(timeout=None)
        self.value = None
        self.ctx = ctx
        self.button_name = button_name
        self.button_id = button_id
        self.button_flags = button_flags
        self.button_args = button_args
        self.button_ispreset = button_ispreset
        self.button_mtype = button_mtype

    @discord.ui.select(
        min_values=1,
        max_values=16,
        options=[
            discord.SelectOption(
                label="Tunes",
                emoji="<:maria:447221707279826944>",
                description="Randomize the music",
            ),
            discord.SelectOption(
                label="ChaoticTunes",
                emoji="<:funkbaba:836700117826142229>",
                description="Chaotically randomize the music",
            ),
            discord.SelectOption(
                label="NoTunes",
                emoji="<:GogoMute:667486074427146252>",
                description="No music, just SFX",
            ),
            discord.SelectOption(
                label="Palette",
                emoji="<:SketchUlty:666902749987733514>",
                description="Randomize sprite color palettes",
            ),
            discord.SelectOption(
                label="Paint",
                emoji="<:yikes:447221708303106048>",
                description="Randomize the sprites, portraits and palettes",
            ),
            discord.SelectOption(
                label="Kupo",
                emoji="<:MogHappy:667477014801809428>",
                description="Everyone's a moogle!",
            ),
            discord.SelectOption(
                label="FancyGau",
                emoji="<:gau_smoosh:956342867897516102>",
                description="He cleans up nice!",
            ),
            discord.SelectOption(
                label="Objectives",
                emoji="<a:KefkaLaugh:666889733301075979>",
                description="Randomize the objectives of the seed",
            ),
            discord.SelectOption(
                label="NoSpoilers",
                emoji="<:StragoNap:667477014793682944>",
                description="Ensure spoiler log IS NOT included",
            ),
            discord.SelectOption(
                label="Spoilers",
                emoji="<:strago_smoosh:956342464548061245>",
                description="Ensure spoiler log IS included",
            ),
            discord.SelectOption(
                label="NoFlashes",
                emoji="<:LeoShock:666915710488018946>",
                description='Forces the "Remove Worst Flashes" flag',
            ),
            discord.SelectOption(
                label="Yeet",
                emoji="<:EdgarChainSaw:666886468953964566>",
                description='Forces the "Y-NPC Remove" flag',
            ),
            discord.SelectOption(
                label="Hundo",
                emoji="<:ff6worGitgud:933089780382716005>",
                description="Forces a 100% complete seed",
            ),
            discord.SelectOption(
                label="Loot",
                emoji="<:LockeCaught:667228085434712077>",
                description="All enemy drops and steals are randomized",
            ),
            discord.SelectOption(
                label="Poverty",
                emoji="<:locke_smoosh:956342711428972597>",
                description="All enemies have NOTHING!",
            ),
            discord.SelectOption(
                label="Mystery",
                emoji="<:what:414522067648643083>",
                description="Hides the flags from the log and track menu",
            ),
            discord.SelectOption(
                label="STEVE",
                emoji="<:Kappa:698619218358304868>",
                description="Everything is and always will be STEVE",
            ),
        ],
        custom_id="re_roll_extra_selector",
    )
    async def extra_select(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        try:
            await interaction.response.defer()
            msg = await interaction.channel.send(
                f"Rerolling a seed for {interaction.user.display_name}"
            )
            return await roll_button_seed(
                self.ctx,
                self.button_name,
                self.button_id,
                self.button_flags,
                " ".join(select.values),
                self.button_ispreset,
                self.button_id.split("_")[2:][0],
                msg,
                True,
            )  # TODO

        except (discord.errors.HTTPException, discord.errors.NotFound):
            await interaction.followup.send(
                "You already rerolled this one...", ephemeral=True
            )

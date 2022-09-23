import discord
from discord.ui import View

import parse_commands


class NewPresetView(View):
    def __init__(self, name, flags, desc, extras) -> None:
        super().__init__(timeout=None)
        self.value = None
        self.name = name
        self.flags = flags
        self.desc = desc
        self.extras = extras

    @discord.ui.button(label="Add Extras", style=discord.ButtonStyle.green, emoji="🎉", custom_id="add_extras_button")
    async def add_item_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("What extras do you want, dirtbag?", ephemeral=True)
        except KeyError:
            await interaction.response.send_message(f"Sorry, this button is out of date! It's just there to look "
                                                    f"pretty now...", ephemeral=True)


class TryItView(View):
    def __init__(self, name, flags, desc, extras):
        super().__init__(timeout=None)
        self.value = None
        self.name = name
        self.flags = flags
        self.desc = desc
        self.extras = extras

    @discord.ui.button(label="Try it!", style=discord.ButtonStyle.green, emoji="🎲", custom_id="roll_preset_button")
    async def try_it(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.name != "":
            await interaction.response.send_message(
                f"Yay it's the {self.name} preset! Here are the flags:\n{self.flags}")
        else:
            await interaction.response.send_message(f"Sorry, this button is out of date! It's just there to look "
                                                    f"pretty now...", ephemeral=True)


class ReRollView(View):
    def __init__(self, message):
        super().__init__(timeout=None)
        self.value = None
        self.message = message

    @discord.ui.button(label="Reroll", style=discord.ButtonStyle.green, emoji="🎲",
                       custom_id="re_roll_button")
    async def reroll(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message != "":
            try:
                await interaction.response.send_message(f'Bundling something up...', ephemeral=True)
                await parse_commands.parse_bot_command(self.message, None, False)
            except (discord.errors.HTTPException, discord.errors.NotFound):
                await interaction.followup.send(f"I'm a little overloaded - give me a sec and try again",
                                                ephemeral=True)
        else:
            await interaction.response.send_message(f"Sorry, this button is out of date! It's just there to look "
                                                    f"pretty now...", ephemeral=True)

    @discord.ui.button(label="Reroll with extras", style=discord.ButtonStyle.green, emoji="<:Lucky:933072743350562886>",
                       custom_id="re_roll_extra_button")
    async def reroll_extra(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.message != "":
                await interaction.response.send_message(f'What do you want to include in your re-roll?',
                                                        view=ReRollExtraView(self.message, interaction), ephemeral=True)
                # await interaction.response.defer()
                # await parse_commands.parse_bot_command(self.message, False, False, False)
            else:
                await interaction.response.send_message(
                    f"Sorry, this button is out of date! It's just there to look "
                    f"pretty now...", ephemeral=True)
        except (discord.errors.HTTPException, discord.errors.NotFound):
            await interaction.response.send_message(f"I'm a little overloaded - give me a sec and try again",
                                                    ephemeral=True)


class ReRollExtraView(View):
    def __init__(self, message, interaction):
        super().__init__(timeout=None)
        self.value = None
        self.message = message
        self.interaction = interaction

    @discord.ui.select(
        min_values=1,
        max_values=17,
        options=[
            discord.SelectOption(label="Splash", emoji="<:HiMog:933072743400865913>",
                                 description="Adds the FF6WC title screen"),
            discord.SelectOption(label="Loot", emoji="<:haha:447221699239215105>",
                                 description="Randomize enemy drops/steals (excluding Dragons, Statues and MiaBs)"),
            discord.SelectOption(label="True Loot", emoji="<:lurk:561376819111264290>",
                                 description="Randomize all enemy drops/steals"),
            discord.SelectOption(label="Poverty", emoji="<:locke_smoosh:956342711428972597>",
                                 description="All enemies have NOTHING!"),
            discord.SelectOption(label="Tunes", emoji="<:maria:447221707279826944>", description="Randomize the music"),
            discord.SelectOption(label="Chaotic Tunes", emoji="<:funkbaba:836700117826142229>",
                                 description="Chaotically randomize the music"),
            discord.SelectOption(label="No Tunes", emoji="<:GogoMute:667486074427146252>",
                                 description="No music, just SFX"),
            discord.SelectOption(label="Palette", emoji="<:SketchUlty:666902749987733514>",
                                 description="Randomize sprite color palettes"),
            discord.SelectOption(label="Paint", emoji="<:yikes:447221708303106048>",
                                 description="Randomize the sprites, portraits and palettes"),
            discord.SelectOption(label="Kupo", emoji="<:MogHappy:667477014801809428>",
                                 description="Everyone's a moogle!"),
            discord.SelectOption(label="Objectives", emoji="<a:KefkaLaugh:666889733301075979>",
                                 description="Randomize the objectives of the seed"),
            discord.SelectOption(label="No Spoiler", emoji="<:StragoNap:667477014793682944>",
                                 description="Ensure no spoiler log"),
            discord.SelectOption(label="No Flashes", emoji="<:LeoShock:666915710488018946>",
                                 description='Forces the "Remove Worst Flashes" flag'),
            discord.SelectOption(label="Yeet", emoji="<:EdgarChainSaw:666886468953964566>",
                                 description='Forces the "Y-NPC Remove" flag'),
            discord.SelectOption(label="Hundo", emoji="<:ff6worGitgud:933089780382716005>",
                                 description="Forces a 100% complete seed"),
            discord.SelectOption(label="Mystery", emoji="<:what:414522067648643083>",
                                 description="Hides the flags from the log and track menu"),
            discord.SelectOption(label="STEVE", emoji="<:Kappa:698619218358304868>",
                                 description="Everything is and always will be STEVE")
        ],
        custom_id='re_roll_extra_selector'
    )
    async def extra_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if select.values != "":
            try:
                await interaction.response.send_message(f'Bundling something up...', ephemeral=True)
                await parse_commands.parse_bot_command(self.message, select.values, True)
            except (discord.errors.HTTPException, discord.errors.NotFound):
                await interaction.followup.send(f"I'm a little overloaded - give me a sec and try again",
                                                ephemeral=True)
        else:
            await interaction.response.send_message(f"Sorry, this button is out of date! It's just there to look "
                                                    f"pretty now...", ephemeral=True)

import discord
from discord.ui import View, TextInput
import parse_commands
from discord import TextStyle, Interaction
import datetime
import json
import os
from config.definitions import ROOT_DIR


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
                await interaction.response.defer()
                await parse_commands.parse_bot_command(self.message, False, False, False)
            except (discord.errors.HTTPException, discord.errors.NotFound):
                await interaction.response.send_message(f"I'm a little overloaded - give me a sec and try again",
                                                        ephemeral=True)
        else:
            await interaction.response.send_message(f"Sorry, this button is out of date! It's just there to look "
                                                    f"pretty now...", ephemeral=True)


    @discord.ui.button(label="Reroll with more", style=discord.ButtonStyle.green, emoji="<:Lucky:933072743350562886>",
                       custom_id="re_roll_extra_button")
    async def reroll_extra(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.message != "":
                await interaction.response.send_message(f'What do you want to include in your re-roll?', view=ReRollExtraView(self.message, interaction), ephemeral=True)
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
        max_values=10,
        options=[
            discord.SelectOption(label="Loot", emoji="<:haha:447221699239215105>", description="Randomize enemy drops/steals (excluding Dragons, Statues and MiaBs)"),
            discord.SelectOption(label="True Loot", emoji="<:lurk:561376819111264290>", description="Randomize all enemy drops/steals"),
            discord.SelectOption(label="Poverty", emoji="<:locke_smoosh:956342711428972597>", description="All enemies have NOTHING!"),
            discord.SelectOption(label="Tunes", emoji="<:maria:447221707279826944>", description="Randomize the music"),
            discord.SelectOption(label="Chaotic Tunes", emoji="<:funkbaba:836700117826142229>",
                                 description="Chaotically randomize the music"),
            discord.SelectOption(label="No Tunes", emoji="<:GogoMute:667486074427146252>",
                                 description="No music, just SFX"),
            discord.SelectOption(label="Palette", emoji="<:SketchUlty:666902749987733514>",
                                 description="Randomize sprite color palettes"),
            discord.SelectOption(label="Paint", emoji="<:yikes:447221708303106048>", description="Randomize the sprites, portraits and palettes"),
            discord.SelectOption(label="Kupo", emoji="<:MogHappy:667477014801809428>",
                                 description="Everyone's a moogle!"),
            discord.SelectOption(label="STEVE", emoji="<:Kappa:698619218358304868>",
                                 description="Everything is and always will be STEVE")
        ],
        custom_id='re_roll_extra_selector'
    )
    async def extra_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_message(f'You selected {select.values}')

    # @discord.ui.button(label="Tunes", style=discord.ButtonStyle.green, emoji="<:maria:447221707279826944>", custom_id="re_roll_tunes_button")
    # async def reroll_tunes(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     try:
    #         if self.message != "":
    #             await interaction.response.defer()
    #             await parse_commands.parse_bot_command(self.message, False, True, False)
    #         else:
    #             await interaction.response.send_message(f"Sorry, this button is out of date! It's just there to look "
    #                                                     f"pretty now...", ephemeral=True)
    #     except (discord.errors.HTTPException, discord.errors.NotFound):
    #         await interaction.response.send_message(f"I'm a little overloaded - give me a sec and try again", ephemeral=True)
    #
    # @discord.ui.button(label="Palette", style=discord.ButtonStyle.green, emoji="<:SketchUlty:666902749987733514>",
    #                    custom_id="re_roll_palette_button")
    # async def reroll_palette(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     try:
    #         if self.message != "":
    #             await interaction.response.defer()
    #             await parse_commands.parse_bot_command(self.message, False, False, True)
    #         else:
    #             await interaction.response.send_message(f"Sorry, this button is out of date! It's just there to look "
    #                                                     f"pretty now...", ephemeral=True)
    #     except (discord.errors.HTTPException, discord.errors.NotFound):
    #         await interaction.response.send_message(f"I'm a little overloaded - give me a sec and try again", ephemeral=True)

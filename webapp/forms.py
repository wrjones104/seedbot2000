import requests
import json
import subprocess
import uuid
import sys
from pathlib import Path

from django import forms
from django.conf import settings
from profanity import profanity
from bot.utils import flag_processor

ARGUMENT_CHOICES = [
    ('paint', 'Paint'), ('kupo', 'Kupo'), ('loot', 'Loot'), ('fancygau', 'Fancy Gau'),
    ('hundo', 'Hundo'), ('objectives', 'Objectives'), ('nospoilers', 'No Spoilers'),
    ('spoilers', 'Spoilers'), ('noflashes', 'No Flashes'), ('dash', 'Dash'),
    ('emptyshops', 'Empty Shops'), ('emptychests', 'Empty Chests'), ('yeet', 'Yeet'),
    ('cg', 'CG'), ('palette', 'Palette'), ('mystery', 'Mystery'), ('doors', 'Doors'),
    ('practice', 'Practice'), ('dev', 'Dev'), ('dungeoncrawl', 'Dungeon Crawl'),
    ('doorslite', 'Doors Lite'), ('doorx', 'Door-X'), ('maps', 'Maps'), ('mapx', 'Map-X'), ('ap', 'AP'),
    ('apts', 'APTS'), ('flagsonly', 'Flags Only'), ('zozo', 'Zozo'),
    ('desc', 'Desc'), ('lg1', 'LG1'), ('lg2', 'LG2'), ('ws', 'WS'), ('csi', 'CSI'),
    ('tunes', 'Tunes'), ('ctunes', 'Chaotic Tunes')
]

LOCAL_ROLL_ARGS = {
    'practice', 'doors', 'dungeoncrawl', 'doorslite', 'doorx', 'maps', 
    'mapx', 'lg1', 'lg2', 'ws', 'csi', 'tunes', 'ctunes', 'zozo', 'dev', 'new'
}

DIR_MAP = {
    'practice': 'WorldsCollide_practice', 'doors': 'WorldsCollide_Door_Rando',
    'dungeoncrawl': 'WorldsCollide_Door_Rando', 'doorslite': 'WorldsCollide_Door_Rando', 'doorx': 'WorldsCollide_Door_Rando',
    'maps': 'WorldsCollide_Door_Rando', 'mapx': 'WorldsCollide_Door_Rando',
    'lg1': 'WorldsCollide_location_gating1', 'lg2': 'WorldsCollide_location_gating1',
    'ws': 'WorldsCollide_shuffle_by_world', 'csi': 'WorldsCollide_shuffle_by_world',
    'dev': 'WorldsCollide_dev', 'new': 'WorldsCollide_dev',
}

class PresetForm(forms.Form):
    preset_name = forms.CharField(max_length=255, label="Preset Name")
    flags = forms.CharField(widget=forms.Textarea, required=False, label="Flags")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Description")
    arguments = forms.MultipleChoiceField(
        choices=ARGUMENT_CHOICES,
        widget=forms.SelectMultiple,
        required=False,
        label="Arguments"
    )
    official = forms.BooleanField(required=False, label="Official")
    hidden = forms.BooleanField(required=False, label="Hide Flags (for mystery seeds)")

    def __init__(self, *args, **kwargs):
        is_official = kwargs.pop('is_official', False)
        preset_instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        
        if preset_instance:
            if hasattr(preset_instance, 'preset_name'):
                self.fields['preset_name'].initial = preset_instance.preset_name
                self.fields['flags'].initial = preset_instance.flags
                self.fields['description'].initial = preset_instance.description
                if preset_instance.arguments:
                    self.fields['arguments'].initial = preset_instance.arguments.split()
                self.fields['official'].initial = preset_instance.official
                self.fields['hidden'].initial = preset_instance.hidden
            else:
                self.fields['preset_name'].initial = preset_instance.get('preset_name', '')
                self.fields['flags'].initial = preset_instance.get('flags', '')
                self.fields['description'].initial = preset_instance.get('description', '')
                if preset_instance.get('arguments'):
                    self.fields['arguments'].initial = preset_instance.get('arguments', '').split()
                self.fields['official'].initial = preset_instance.get('official', False)
                self.fields['hidden'].initial = preset_instance.get('hidden', False)

        if not is_official:
            if 'official' in self.fields:
                self.fields.pop('official')

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("preset_name")
        description = cleaned_data.get("description")
        
        if name and profanity.contains_profanity(name):
            self.add_error('preset_name', "Watch your mouth, dirtbag!")
        if description and profanity.contains_profanity(description):
            self.add_error('description', "Watch your mouth, dirtbag!")
        
        return cleaned_data


class TuneUpForm(forms.Form):
    rom_file = forms.FileField(
        label='Upload a .sfc, .smc, or .zip file',
        widget=forms.ClearableFileInput(attrs={'accept': '.sfc,.smc,.zip'})
    )
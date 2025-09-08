import requests
import json
import subprocess
import uuid
import sys
from pathlib import Path

from django import forms
from django.conf import settings
from .models import Preset
from profanity import profanity
from bot.utils import flag_processor

ARGUMENT_CHOICES = [
    ('paint', 'Paint'), ('kupo', 'Kupo'), ('loot', 'Loot'), ('fancygau', 'Fancy Gau'),
    ('hundo', 'Hundo'), ('objectives', 'Objectives'), ('nospoilers', 'No Spoilers'),
    ('spoilers', 'Spoilers'), ('noflashes', 'No Flashes'), ('dash', 'Dash'),
    ('emptyshops', 'Empty Shops'), ('emptychests', 'Empty Chests'), ('yeet', 'Yeet'),
    ('cg', 'CG'), ('palette', 'Palette'), ('mystery', 'Mystery'), ('doors', 'Doors'),
    ('practice', 'Practice'), ('dev', 'Dev'), ('dungeoncrawl', 'Dungeon Crawl'),
    ('doorslite', 'Doors Lite'), ('maps', 'Maps'), ('mapx', 'Map-X'), ('ap', 'AP'),
    ('apts', 'APTS'), ('flagsonly', 'Flags Only'), ('zozo', 'Zozo'),
    ('desc', 'Desc'), ('lg1', 'LG1'), ('lg2', 'LG2'), ('ws', 'WS'), ('csi', 'CSI'),
    ('tunes', 'Tunes'), ('ctunes', 'Chaotic Tunes')
]

LOCAL_ROLL_ARGS = {
    'practice', 'doors', 'dungeoncrawl', 'doorslite', 'maps', 
    'mapx', 'lg1', 'lg2', 'ws', 'csi', 'tunes', 'ctunes', 'zozo'
}

DIR_MAP = {
    'practice': 'WorldsCollide_practice', 'doors': 'WorldsCollide_Door_Rando',
    'dungeoncrawl': 'WorldsCollide_Door_Rando', 'doorslite': 'WorldsCollide_Door_Rando',
    'maps': 'WorldsCollide_Door_Rando', 'mapx': 'WorldsCollide_Door_Rando',
    'lg1': 'WorldsCollide_location_gating1', 'lg2': 'WorldsCollide_location_gating1',
    'ws': 'WorldsCollide_shuffle_by_world', 'csi': 'WorldsCollide_shuffle_by_world',
}

class PresetForm(forms.ModelForm):
    arguments = forms.MultipleChoiceField(
        choices=ARGUMENT_CHOICES,
        widget=forms.SelectMultiple,
        required=False,
        label="Arguments"
    )

    def __init__(self, *args, **kwargs):
        is_official = kwargs.pop('is_official', False)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.arguments:
            self.fields['arguments'].initial = self.instance.arguments.split()
        if not is_official:
            if 'official' in self.fields:
                self.fields.pop('official')

    def save(self, commit=True):
        # When flags or arguments change, reset validation status
        if self.has_changed() and ('flags' in self.changed_data or 'arguments' in self.changed_data):
            self.instance.validation_status = 'PENDING'
            self.instance.validation_error = None
            
        selected_args = self.cleaned_data.get('arguments', [])
        self.instance.arguments = ' '.join(selected_args)
        return super().save(commit=commit)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("preset_name")
        description = cleaned_data.get("description")
        
        if name and profanity.contains_profanity(name):
            self.add_error('preset_name', "Watch your mouth, dirtbag!")
        if description and profanity.contains_profanity(description):
            self.add_error('description', "Watch your mouth, dirtbag!")
        
        return cleaned_data

    class Meta:
        model = Preset
        fields = ['preset_name','flags','description','arguments','official','hidden']
        labels = {'hidden': 'Hide Flags (for mystery seeds)',}


class TuneUpForm(forms.Form):
    rom_file = forms.FileField(
        label='Upload a .sfc, .smc, or .zip file',
        widget=forms.ClearableFileInput(attrs={'accept': '.sfc,.smc,.zip'})
    )
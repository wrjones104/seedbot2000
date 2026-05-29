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
    ('doorslite', 'Doors Lite'), ('doorx', 'Door-X'), ('maps', 'Maps'), ('mapx', 'Map-X'),
    ('flagsonly', 'Flags Only'), ('zozo', 'Zozo'),
    ('desc', 'Desc'), ('lg1', 'LG1'), ('lg2', 'LG2'), ('ws', 'WS'), ('csi', 'CSI'),
    ('tunes', 'Tunes'), ('ctunes', 'Chaotic Tunes'), ('shoplimits', 'Shop Limits'),
    ('ruin', 'Ruination'), ('jones', 'Jones Dev'), ('who', 'Whos There')
]

LOCAL_ROLL_ARGS = {
    'practice', 'doors', 'dungeoncrawl', 'doorslite', 'doorx', 'maps', 
    'mapx', 'lg1', 'lg2', 'ws', 'csi', 'tunes', 'ctunes', 'zozo', 'dev', 'new'
}

DIR_MAP = {
    'practice': 'WorldsCollide_practice', 'doors': 'WorldsCollide_ruination',
    'dungeoncrawl': 'WorldsCollide_ruination', 'doorslite': 'WorldsCollide_ruination', 'doorx': 'WorldsCollide_ruination',
    'maps': 'WorldsCollide_ruination', 'mapx': 'WorldsCollide_ruination',
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
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        
        if self.instance:
            if hasattr(self.instance, 'preset_name'):
                self.fields['preset_name'].initial = self.instance.preset_name
                self.fields['flags'].initial = self.instance.flags
                self.fields['description'].initial = self.instance.description
                if self.instance.arguments:
                    self.fields['arguments'].initial = self.instance.arguments.split()
                self.fields['official'].initial = self.instance.official
                self.fields['hidden'].initial = self.instance.hidden
            else:
                self.fields['preset_name'].initial = self.instance.get('preset_name', '')
                self.fields['flags'].initial = self.instance.get('flags', '')
                self.fields['description'].initial = self.instance.get('description', '')
                if self.instance.get('arguments'):
                    self.fields['arguments'].initial = self.instance.get('arguments', '').split()
                self.fields['official'].initial = self.instance.get('official', False)
                self.fields['hidden'].initial = self.instance.get('hidden', False)

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

        if name:
            # Case-insensitive uniqueness check
            from bot.utils.firestore_client import db, FirestorePresetAdapter, sanitize_preset_name
            preset_name_lower = name.lower()
            query = db.collection("presets").where("preset_name_lower", "==", preset_name_lower).limit(1).get()
            if query:
                existing_preset = FirestorePresetAdapter(query[0].to_dict(), doc_id=query[0].id)
                instance_name = self.instance.preset_name if hasattr(self.instance, 'preset_name') else (self.instance.get('preset_name') if isinstance(self.instance, dict) else None)
                if not self.instance or (instance_name and sanitize_preset_name(existing_preset.preset_name) != sanitize_preset_name(instance_name)):
                    self.add_error('preset_name', f"A preset with the name '{existing_preset.preset_name}' already exists.")
        
        return cleaned_data


class TuneUpForm(forms.Form):
    rom_file = forms.FileField(
        label='Upload a .sfc, .smc, or .zip file',
        widget=forms.ClearableFileInput(attrs={'accept': '.sfc,.smc,.zip'})
    )
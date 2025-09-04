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
        selected_args = self.cleaned_data.get('arguments', [])
        self.instance.arguments = ' '.join(selected_args)
        return super().save(commit=commit)

    def _validate_flags_locally(self, flags, arguments):
        """Uses a local wc.py script to validate flags."""
        final_flags = flag_processor.apply_args(flags, arguments)
        
        project_root = settings.BASE_DIR
        randomizer_forks_dir = project_root / 'randomizer_forks'

        
        script_dir_name = 'WorldsCollide'
        for arg in arguments:
            if arg in DIR_MAP:
                script_dir_name = DIR_MAP[arg]
                break
        
        script_dir = randomizer_forks_dir / script_dir_name
        wc_script = script_dir / 'wc.py'
        input_smc = project_root / 'data' / 'ff3.smc'
        output_dir = project_root / 'data' / 'seeds'
        output_dir.mkdir(exist_ok=True)
        
        temp_filename = f"validation_{uuid.uuid4().hex[:8]}.smc"
        temp_output_smc = output_dir / temp_filename

        command = [sys.executable, str(wc_script), "-i", str(input_smc), "-o", str(temp_output_smc)]
        command.extend(final_flags.split())

        try:
            subprocess.run(
                command, cwd=script_dir, capture_output=True, text=True,
                timeout=120, check=True
            )
        except subprocess.CalledProcessError as e:
            error_details = e.stderr or e.stdout
            self.add_error('flags', f"Invalid Flags (local validation): {error_details}")
        finally:
            temp_output_smc.unlink(missing_ok=True)
            temp_output_smc.with_suffix('.txt').unlink(missing_ok=True)

    def _validate_flags_api(self, flags):
        """Uses the public API to validate flags."""
        api_url = "https://api.ff6worldscollide.com/api/seed"
        payload = {"key": settings.WC_API_KEY, "flags": flags}
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(api_url, data=json.dumps(payload), headers=headers, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            error_message = "These flags are invalid."
            if e.response:
                try:
                    api_error = e.response.json().get('error', 'API returned an error.')
                    error_message = f"Invalid Flags (API validation): {api_error}"
                except json.JSONDecodeError:
                    error_message = "Invalid Flags: The API returned an unreadable error."
            self.add_error('flags', error_message)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("preset_name")
        description = cleaned_data.get("description")
        flags = cleaned_data.get("flags")
        arguments = cleaned_data.get("arguments", [])

        if name and profanity.contains_profanity(name):
            self.add_error('preset_name', "Watch your mouth, dirtbag!")
        if description and profanity.contains_profanity(description):
            self.add_error('description', "Watch your mouth, dirtbag!")
        if self.errors:
            return cleaned_data

        if flags:
            if any(arg in LOCAL_ROLL_ARGS for arg in arguments):
                self._validate_flags_locally(flags, arguments)
            else:
                self._validate_flags_api(flags)
        
        return cleaned_data

    class Meta:
        model = Preset
        fields = ['preset_name','flags','description','arguments','official','hidden']
        labels = {'hidden': 'Hide Flags (for mystery seeds)',}
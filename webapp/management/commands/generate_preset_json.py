import json
from django.core.management.base import BaseCommand
from django.conf import settings
from webapp.models import Preset

class Command(BaseCommand):
    help = 'Generates a JSON file of presets for external sites to consume.'

    def handle(self, *args, **options):
        self.stdout.write('Starting preset JSON generation...')
        presets = Preset.objects.all()
        self.stdout.write(self.style.WARNING('Including ALL presets (including unofficial and hidden).'))

        preset_dict = {}
        for preset in presets:
            preset_dict[preset.preset_name] = {
                "name": preset.preset_name,
                "creator_id": preset.creator_id,
                "creator_name": preset.creator_name,
                "flags": preset.flags,
                "description": preset.description,
                "arguments": preset.arguments or "",
                "official": preset.official,
                "hidden": preset.hidden,
            }
        
        output_path = settings.BASE_DIR / "data" / "user_presets.json"

        try:
            with open(output_path, "w") as f:
                json.dump(preset_dict, f, indent=4)
            self.stdout.write(self.style.SUCCESS(f'✅ Successfully generated presets.json with {len(preset_dict)} presets.'))
            self.stdout.write(f'   File located at: {output_path}')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred while writing the file: {e}'))
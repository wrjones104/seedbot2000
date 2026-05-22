import json
from django.core.management.base import BaseCommand
from django.conf import settings
from bot.utils.firestore_client import db

class Command(BaseCommand):
    help = 'Generates a JSON file of presets for external sites to consume.'

    def handle(self, *args, **options):
        self.stdout.write('Starting preset JSON generation...')
        presets = db.collection("presets").stream()
        self.stdout.write(self.style.WARNING('Including ALL presets (including unofficial and hidden).'))

        preset_dict = {}
        for doc in presets:
            data = doc.to_dict()
            name = data.get("preset_name", doc.id)
            preset_dict[name] = {
                "name": name,
                "creator_id": str(data.get("creator_id", "")),
                "creator_name": data.get("creator_name", ""),
                "flags": data.get("flags", ""),
                "description": data.get("description", ""),
                "arguments": data.get("arguments", "") or "",
                "official": bool(data.get("official", False)),
                "hidden": bool(data.get("hidden", False)),
            }
        
        output_path = settings.BASE_DIR / "data" / "user_presets.json"

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(preset_dict, f, indent=4)
            self.stdout.write(self.style.SUCCESS(f'Successfully generated presets.json with {len(preset_dict)} presets.'))
            self.stdout.write(f'   File located at: {output_path}')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
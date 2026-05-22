from django.core.management.base import BaseCommand
from webapp.tasks import validate_preset_task
from bot.utils.firestore_client import db

class Command(BaseCommand):
    help = 'Finds all presets with a "PENDING" or "INVALID" validation status and queues a validation task for them.'

    def handle(self, *args, **options):
        self.stdout.write('Checking presets in Firestore...')
        query = db.collection("presets").where("validation_status", "in", ["PENDING", "INVALID"])
        presets_to_validate = list(query.stream())
        
        count = len(presets_to_validate)
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No presets are pending or require re-validation.'))
            return

        self.stdout.write(f'Found {count} presets pending or requiring re-validation. Queueing tasks now...')

        for doc in presets_to_validate:
            data = doc.to_dict()
            name = data.get("preset_name", doc.id)
            status = data.get("validation_status", "PENDING")
            self.stdout.write(f'  -> Queueing validation for: {name} (Status: {status})')
            validate_preset_task.delay(name)

        self.stdout.write(self.style.SUCCESS(f'Successfully queued {count} validation tasks.'))
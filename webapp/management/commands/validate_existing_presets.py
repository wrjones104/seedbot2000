from django.core.management.base import BaseCommand
from webapp.models import Preset
from webapp.tasks import validate_preset_task

class Command(BaseCommand):
    help = 'Finds all presets with a "PENDING" or "INVALID" validation status and queues a validation task for them.'

    def handle(self, *args, **options):
        presets_to_validate = Preset.objects.filter(
            validation_status__in=['PENDING', 'INVALID']
        )
        
        count = presets_to_validate.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS('✔️ No presets are pending or require re-validation.'))
            return

        self.stdout.write(f'Found {count} presets pending or requiring re-validation. Queueing tasks now...')

        for preset in presets_to_validate:
            self.stdout.write(f'  -> Queueing validation for: {preset.preset_name} (Status: {preset.validation_status})')
            validate_preset_task.delay(preset.pk)

        self.stdout.write(self.style.SUCCESS(f'✅ Successfully queued {count} validation tasks.'))
import os
import time
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Deletes seed files from the media directory that are older than 30 days.'

    def handle(self, *args, **options):
        self.stdout.write('Starting cleanup of old seed files...')
        
        seeds_dir = Path(settings.MEDIA_ROOT)
        if not seeds_dir.is_dir():
            self.stdout.write(self.style.ERROR(f"Directory not found: {seeds_dir}"))
            return

        retention_period_seconds = 90 * 24 * 60 * 60
        now = time.time()
        files_deleted = 0

        for file_path in seeds_dir.glob('*.zip'):
            if file_path.is_file():
                try:
                    file_mod_time = os.path.getmtime(file_path)
                    if (now - file_mod_time) > retention_period_seconds:
                        file_path.unlink() # Delete the file
                        self.stdout.write(f'Deleted old file: {file_path.name}')
                        files_deleted += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing {file_path.name}: {e}"))
        
        self.stdout.write(self.style.SUCCESS(f'Cleanup complete. Deleted {files_deleted} file(s).'))
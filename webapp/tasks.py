import zipfile
import shutil
import subprocess
import uuid
import sys
import time
from pathlib import Path
from datetime import datetime

from celery import shared_task
from celery.exceptions import Ignore
from django.conf import settings
from django.db.models import F

from webapp.models import Preset, SeedLog
from bot.utils import flag_processor
from bot.utils.run_local import generate_local_seed, RollException
from bot.utils.tunes_processor import apply_tunes
from bot.utils.metric_writer import write_gsheets
from bot.utils.zip_seed import create_seed_zip


def _robust_delete(file_path, retries=3, delay=0.1):
    """Attempts to delete a file, retrying on PermissionError."""
    for i in range(retries):
        try:
            if file_path.exists():
                file_path.unlink()
            return
        except PermissionError:
            if i < retries - 1:
                time.sleep(delay)
            else:
                print(f"Warning: Could not delete temporary file {file_path} after {retries} attempts.")
        except Exception as e:
            print(f"Warning: An unexpected error occurred while deleting {file_path}: {e}")
            return


@shared_task(bind=True)
def create_local_seed_task(self, preset_pk, discord_id, user_name):
    try:
        preset = Preset.objects.get(pk=preset_pk)
        args_list = preset.arguments.split() if preset.arguments else []
        
        dev_type = None
        tunes_type = None
        for arg in args_list:
            arg_lower = arg.lower()
            if arg_lower in ('practice', 'doors', 'dungeoncrawl', 'doorslite', 'maps', 'mapx', 'lg1', 'lg2', 'ws', 'csi'):
                dev_type = arg_lower
            elif arg_lower in ('tunes', 'ctunes', 'notunes'):
                tunes_type = arg_lower

        ARG_TO_FORK_MAP = {
            'practice': 'practice',
            'dungeoncrawl': 'doors',
            'doorslite': 'doors',
            'maps': 'doors',
            'mapx': 'doors',
            'lg1': 'lg1',
            'lg2': 'lg1',
            'ws': 'ws',
            'csi': 'ws'
        }

        fork_key = dev_type
        if dev_type:
            fork_key = ARG_TO_FORK_MAP.get(dev_type, dev_type)

        self.update_state(state='PROGRESS', meta={'status': 'Generating Seed...'})
        
        final_flags = flag_processor.apply_args(preset.flags, args_list)
        seed_path, seed_id, seed_hash = generate_local_seed(flags=final_flags, seed_type=fork_key)

        if tunes_type:
            self.update_state(state='PROGRESS', meta={'status': f'Applying {tunes_type}...'})
            apply_tunes(smc_path=seed_path, tunes_type=tunes_type)

        self.update_state(state='PROGRESS', meta={'status': 'Packaging Seed...'})
        mtype = f"preset_{preset.preset_name.replace(' ', '_')}"
        has_music_spoiler = tunes_type is not None
        zip_path = create_seed_zip(seed_path, mtype, has_music_spoiler)

        final_destination = Path(settings.MEDIA_ROOT) / zip_path.name
        shutil.move(zip_path, final_destination)

        preset.gen_count = F('gen_count') + 1
        preset.save(update_fields=['gen_count'])
        
        share_url = f'{settings.MEDIA_URL}{zip_path.name}'
        timestamp = datetime.now().strftime('%b %d %Y %H:%M:%S')
        has_paint = bool(preset.arguments and 'paint' in preset.arguments.lower())

        log_entry = {
            'creator_id': discord_id,
            'creator_name': user_name,
            'seed_type': preset.preset_name,
            'share_url': share_url,
            'timestamp': timestamp,
            'server_name': 'WebApp',
            'server_id': None,
            'channel_name': None,
            'channel_id': None,
            'random_sprites': has_paint
        }
        
        SeedLog.objects.create(**log_entry)
        write_gsheets(log_entry)

        return share_url

    except (RollException, Exception) as e:
        error_message = str(e)
        if hasattr(e, 'sperror'):
            error_message = e.sperror
        
        self.update_state(state='FAILURE', meta={'exc_type': type(e).__name__, 'exc_message': error_message})
        raise Ignore()

@shared_task
def validate_preset_task(preset_pk):
    """
    A background task to validate preset flags locally without blocking the web server.
    This will use the appropriate local randomizer fork for all presets.
    """
    preset = None
    try:
        preset = Preset.objects.get(pk=preset_pk)
        args_list = preset.arguments.split() if preset.arguments else []
        
        from webapp.forms import DIR_MAP

        final_flags = flag_processor.apply_args(preset.flags, args_list)
        
        script_dir_name = 'WorldsCollide'
        for arg in args_list:
            if arg in DIR_MAP:
                script_dir_name = DIR_MAP[arg]
                break
        
        script_dir = settings.BASE_DIR / 'randomizer_forks' / script_dir_name
        wc_script = script_dir / 'wc.py'
        input_smc = settings.BASE_DIR / 'data' / 'ff3.smc'
        output_dir = settings.BASE_DIR / 'data' / 'seeds'
        output_dir.mkdir(exist_ok=True)
        temp_output_smc = output_dir / f"validation_{uuid.uuid4().hex[:8]}.smc"

        command = [sys.executable, str(wc_script), "-i", str(input_smc), "-o", str(temp_output_smc)]
        command.extend(final_flags.split())

        try:
            subprocess.run(
                command, cwd=script_dir, capture_output=True, text=True,
                timeout=120, check=True
            )
            preset.validation_status = 'VALID'
            preset.validation_error = None
        except subprocess.CalledProcessError as e:
            preset.validation_status = 'INVALID'
            preset.validation_error = e.stderr or e.stdout
        finally:
            _robust_delete(temp_output_smc)
            _robust_delete(temp_output_smc.with_suffix('.txt'))

    except Preset.DoesNotExist:
        return
    except Exception as e:
        if preset:
            preset.validation_status = 'INVALID'
            preset.validation_error = f"An unexpected error occurred during validation: {str(e)}"
    finally:
        if preset:
            preset.save()

@shared_task(bind=True)
def apply_tunes_task(self, temp_file_path_str, tunes_type):
    """
    Celery task to apply music randomization to an uploaded ROM file.
    """
    try:
        self.update_state(state='PROGRESS', meta={'status': 'Preparing ROM...'})
        temp_file_path = Path(temp_file_path_str)
        
        # Directory for final, tuned ROMs, accessible via MEDIA_URL
        output_dir = Path(settings.MEDIA_ROOT) / 'tuned_roms'
        output_dir.mkdir(exist_ok=True)
        
        rom_to_process = None

        if temp_file_path.suffix.lower() == '.zip':
            self.update_state(state='PROGRESS', meta={'status': 'Unzipping archive...'})
            with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
                for member in zip_ref.infolist():
                    if member.filename.lower().endswith(('.sfc', '.smc')):
                        # Extract with a unique name to the output directory
                        extracted_filename = f"{uuid.uuid4()}_{Path(member.filename).name}"
                        rom_to_process = output_dir / extracted_filename
                        with open(rom_to_process, 'wb') as rom_file:
                            rom_file.write(zip_ref.read(member.filename))
                        break
                if not rom_to_process:
                    raise ValueError("No .sfc or .smc file found in the zip archive.")
        elif temp_file_path.suffix.lower() in ['.sfc', '.smc']:
            # Move the original file to the output directory to process it there
            new_path = output_dir / temp_file_path.name
            temp_file_path.rename(new_path)
            rom_to_process = new_path
        else:
            raise ValueError("Invalid file type. Please upload a .sfc, .smc, or .zip file.")

        self.update_state(state='PROGRESS', meta={'status': f'Applying {tunes_type} tunes...'})
        apply_tunes(rom_to_process, tunes_type)
        
        # Clean up the original uploaded file from the temp directory
        if temp_file_path.exists():
            temp_file_path.unlink()

        # The result of the task is the URL to the tuned ROM
        file_url = f"{settings.MEDIA_URL}tuned_roms/{rom_to_process.name}"
        return file_url

    except Exception as e:
        # If anything goes wrong, clean up any files that might have been created
        if 'temp_file_path' in locals() and temp_file_path.exists():
            temp_file_path.unlink()
        if 'rom_to_process' in locals() and rom_to_process.exists():
            rom_to_process.unlink()
        
        # Propagate the exception so the task state becomes 'FAILURE'
        raise e
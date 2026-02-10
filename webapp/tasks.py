import zipfile
import shutil
import subprocess
import uuid
import sys
import time    
import requests
import json
import traceback
from pathlib import Path
from datetime import datetime
import tempfile

from celery import shared_task
from celery.exceptions import Ignore
from django.conf import settings
from django.db.models import F
from django.utils import timezone

from webapp.models import Preset, SeedLog
from bot import flag_builder
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


@shared_task
def log_seed_stats_task(log_entry):
    try:
        # Convert timestamp string back to datetime if necessary, or let write_gsheets handle it
        # write_gsheets expects a dict where 'timestamp' is used.
        # It calls str(m['timestamp']), so a string is fine.
        write_gsheets(log_entry)
    except Exception as e:
        print(f"Error logging to GSheets (async): {e}")


def _generate_seed_core(task, base_flags, args_list, seed_type_name, creator_id, creator_name, preset=None):
    temp_dir = None
    try:
        temp_dir = Path(tempfile.mkdtemp())
        
        practice_args_str = ""
        is_practice_roll = False
        if 'practice_easy' in args_list:
            is_practice_roll = True
        elif 'practice_medium' in args_list:
            is_practice_roll = True
            practice_args_str = "--ul"
        elif 'practice_hard' in args_list:
            is_practice_roll = True
            practice_args_str = "--hard"
            
        if is_practice_roll:
            task.update_state(state='PROGRESS', meta={'status': 'Generating Dynamic Practice Flags...'})
            final_flags = flag_builder.practice(practice_args_str)
            if 'practice' not in args_list:
                args_list.append('practice')
        else:
            final_flags = flag_processor.apply_args(base_flags, args_list)

        dev_type = None
        tunes_type = None
        for arg in args_list:
            arg_lower = arg.lower()
            if arg_lower in ('practice', 'doors', 'dungeoncrawl', 'doorslite', 'doorx', 'maps', 'mapx', 'lg1', 'lg2', 'ws', 'csi'):
                dev_type = arg_lower
            elif arg_lower in ('tunes', 'ctunes', 'notunes'):
                tunes_type = arg_lower

        ARG_TO_FORK_MAP = {
            'practice': 'practice',
            'dungeoncrawl': 'doors',
            'doorslite': 'doors',
            'doorx': 'doors',
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

        task.update_state(state='PROGRESS', meta={'status': 'Generating Seed...'})
        
        seed_path, seed_id, seed_hash = generate_local_seed(
            flags=final_flags, 
            seed_type=fork_key, 
            output_dir=temp_dir
        )

        if tunes_type:
            task.update_state(state='PROGRESS', meta={'status': f'Applying {tunes_type}...'})
            with open(seed_path, 'rb') as f:
                in_rom_bytes = f.read()
            
            tuned_rom_bytes, music_spoiler_content = apply_tunes(in_rom_bytes, tunes_type=tunes_type)
            
            with open(seed_path, 'wb') as f:
                f.write(tuned_rom_bytes)
            
            spoiler_path = seed_path.with_suffix('.txt').with_stem(f"{seed_path.stem}_music_spoiler")
            with open(spoiler_path, 'w', encoding='utf-8') as f:
                f.write(music_spoiler_content)

        task.update_state(state='PROGRESS', meta={'status': 'Packaging Seed...'})
        safe_seed_type = seed_type_name.replace(' ', '_')
        mtype = f"preset_{safe_seed_type}"
        has_music_spoiler = tunes_type is not None
        zip_path = create_seed_zip(seed_path, mtype, has_music_spoiler)

        final_destination = Path(settings.MEDIA_ROOT) / zip_path.name
        shutil.move(zip_path, final_destination)

        if preset:
            preset.gen_count = F('gen_count') + 1
            preset.save(update_fields=['gen_count'])
        
        share_url = f'{settings.MEDIA_URL}{zip_path.name}'
        # Check for paint argument in various forms (with or without hyphen)
        has_paint = False
        if args_list:
            args_lower = [arg.lower() for arg in args_list]
            has_paint = 'paint' in args_lower or '-paint' in args_lower or '--paint' in args_lower

        log_entry = {
            'creator_id': creator_id,
            'creator_name': creator_name,
            'seed_type': seed_type_name,
            'share_url': share_url,
            'timestamp': timezone.now(),
            'server_name': 'WebApp',
            'server_id': None,
            'channel_name': None,
            'channel_id': None,
            'random_sprites': has_paint,
            'hash': seed_hash,
            'seed': seed_id
        }
        
        SeedLog.objects.create(**log_entry)

        # Prepare log entry for async task (ensure serializable)
        async_log_entry = log_entry.copy()
        if isinstance(async_log_entry.get('timestamp'), datetime):
            async_log_entry['timestamp'] = async_log_entry['timestamp'].isoformat()

        log_seed_stats_task.delay(async_log_entry)

        # Explicitly set the task state to SUCCESS with the result.
        # This is redundant if the function returns normally, but helps ensure
        # the PROGRESS state is definitely overwritten immediately.
        task.update_state(state='SUCCESS', meta=share_url)

        return share_url

    except (RollException, Exception) as e:
        error_message = str(e)
        if hasattr(e, 'sperror'):
            error_message = e.sperror
        
        task.update_state(state='FAILURE', meta={'exc_type': type(e).__name__, 'exc_message': error_message})
        raise Ignore()
    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)


@shared_task(bind=True)
def create_local_seed_task(self, preset_pk, discord_id, user_name):
    try:
        preset = Preset.objects.get(pk=preset_pk)
        args_list = preset.arguments.split() if preset.arguments else []
        result_url = _generate_seed_core(self, preset.flags, args_list, preset.preset_name, discord_id, user_name, preset=preset)
        self.update_state(state='SUCCESS', meta=result_url)
        return result_url
    except Preset.DoesNotExist:
        self.update_state(state='FAILURE', meta={'exc_type': 'Preset.DoesNotExist', 'exc_message': 'Preset not found'})
        raise Ignore()

@shared_task(bind=True)
def create_api_seed_generation_task(self, flags, args_list, seed_type_name, creator_id, creator_name):
    preset_obj = None
    # seed_type_name could be a preset name or a custom string like "API - Custom"
    # We only want to increment gen_count if it's an actual preset.
    # Preset pk is the preset_name string.
    try:
        preset_obj = Preset.objects.get(preset_name=seed_type_name)
    except (Preset.DoesNotExist, ValueError):
        pass

    result_url = _generate_seed_core(self, flags, args_list, seed_type_name, creator_id, creator_name, preset=preset_obj)
    self.update_state(state='SUCCESS', meta=result_url)
    return result_url


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
    temp_file_path = Path(temp_file_path_str)
    tuned_rom_path = None
    try:
        self.update_state(state='PROGRESS', meta={'status': 'Preparing ROM...'})
        
        output_dir = Path(settings.MEDIA_ROOT) / 'tuned_roms'
        output_dir.mkdir(exist_ok=True)

        # Define a unique name for the final output file
        tuned_rom_name = f"{uuid.uuid4().hex[:12]}_{tunes_type}.smc"
        tuned_rom_path = output_dir / tuned_rom_name
        
        # Read the uploaded file into an in-memory bytes object
        if temp_file_path.suffix.lower() == '.zip':
            self.update_state(state='PROGRESS', meta={'status': 'Unzipping archive...'})
            with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
                for member in zip_ref.infolist():
                    if member.filename.lower().endswith(('.sfc', '.smc')):
                        in_rom_bytes = zip_ref.read(member.filename)
                        break
                else:
                    raise ValueError("No .sfc or .smc file found in the zip archive.")
        elif temp_file_path.suffix.lower() in ['.sfc', '.smc']:
            with open(temp_file_path, 'rb') as f:
                in_rom_bytes = f.read()
        else:
            raise ValueError("Invalid file type. Please upload a .sfc, .smc, or .zip file.")

        self.update_state(state='PROGRESS', meta={'status': f'Applying {tunes_type} tunes...'})
        
        # Process the bytes in memory, getting back the tuned bytes and spoiler text
        tuned_rom_bytes, music_spoiler_content = apply_tunes(in_rom_bytes, tunes_type)

        # Write the modified bytes to a brand new file, which this worker will own
        with open(tuned_rom_path, 'wb') as f:
            f.write(tuned_rom_bytes)
        
        # Write the music spoiler to its own file
        spoiler_path = tuned_rom_path.with_suffix('.txt')
        with open(spoiler_path, 'w', encoding="utf-8") as f:
            f.write(music_spoiler_content)

        # Clean up the original uploaded file from the temp directory
        _robust_delete(temp_file_path)

        file_url = f"{settings.MEDIA_URL}tuned_roms/{tuned_rom_path.name}"
        return file_url

    except Exception as e:
        # Cleanup and Error Reporting
        _robust_delete(temp_file_path)
        if tuned_rom_path:
            _robust_delete(tuned_rom_path)
            _robust_delete(tuned_rom_path.with_suffix('.txt'))
        
        error_string = str(e)
        user_message = f"An unexpected error occurred while processing the ROM. Details: {error_string}"

        if "FreeSpaceError" in error_string or "Not enough free space" in error_string:
            user_message = "Could not apply tunes. The ROM is likely not a compatible FF6 ROM or already has music randomization applied."
        elif isinstance(e, ValueError):
            user_message = error_string

        self.update_state(
            state='FAILURE',
            meta={'exc_type': type(e).__name__, 'exc_message': user_message}
        )
        raise Ignore()


@shared_task(bind=True)
def create_api_seed_task(self, preset_pk, discord_id, user_name):
    try:
        preset = Preset.objects.get(pk=preset_pk)
        args_list = preset.arguments.split() if preset.arguments else []

        
        # This logic handles on-the-fly flag generation for quick rolls
        if preset.preset_name == "Quick Roll - Rando":
            final_flags = flag_builder.standard()
        elif preset.preset_name == "Quick Roll - Chaos":
            final_flags = flag_builder.chaos()
        elif preset.preset_name == "Quick Roll - True Chaos":
            final_flags = flag_builder.true_chaos()
        else:
            final_flags = flag_processor.apply_args(preset.flags, args_list)

        self.update_state(state='PROGRESS', meta={'status': 'Contacting Worlds Collide API...'})
        
        api_url = "https://api.ff6worldscollide.com/api/seed"
        payload = {"key": settings.WC_API_KEY, "flags": final_flags}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(api_url, data=json.dumps(payload), headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        seed_url = data.get('url')
        seed_id = data.get('seed_id')
        seed_hash = data.get('hash')

        preset.gen_count = F('gen_count') + 1
        preset.save(update_fields=['gen_count'])

        has_paint = bool(preset.arguments and 'paint' in preset.arguments.lower())

        log_entry = {
            'creator_id': discord_id, 'creator_name': user_name, 'seed_type': preset.preset_name,
            'share_url': seed_url, 'timestamp': timezone.now(), 'server_name': 'WebApp',
            'random_sprites': has_paint, 'server_id': None, 'channel_name': None, 'channel_id': None,
            'hash': seed_hash, 'seed': seed_id
        }
        SeedLog.objects.create(**log_entry)

        self.update_state(state='PROGRESS', meta={'status': 'Finalizing Seed...'})

        # Prepare log entry for async task (ensure serializable)
        async_log_entry = log_entry.copy()
        if isinstance(async_log_entry.get('timestamp'), datetime):
            async_log_entry['timestamp'] = async_log_entry['timestamp'].isoformat()

        log_seed_stats_task.delay(async_log_entry)

        # Explicitly set the task state to SUCCESS with the result.
        self.update_state(state='SUCCESS', meta=seed_url)

        return seed_url

    except requests.exceptions.RequestException as e:
        error_message = "The FF6WC API could not be reached or returned an error. Please try again later."
        if e.response:
            try:
                api_error = e.response.json().get('error', 'Unspecified API error.')
                error_message = f"API Error: {api_error}"
            except json.JSONDecodeError:
                error_message = "The FF6WC API returned an unreadable error."
        
        self.update_state(state='FAILURE', meta={'exc_type': type(e).__name__, 'exc_message': error_message})
        raise Ignore()
    except Exception as e:
        self.update_state(state='FAILURE', meta={'exc_type': type(e).__name__, 'exc_message': str(e)})
        raise Ignore()
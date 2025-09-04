import zipfile
import shutil
import asyncio
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
        seed_path, seed_id, seed_hash = asyncio.run(generate_local_seed(flags=final_flags, seed_type=fork_key))

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
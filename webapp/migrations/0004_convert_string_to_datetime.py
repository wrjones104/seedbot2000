# in webapp/migrations/00XY_convert_string_to_datetime.py

from django.db import migrations
from django.utils import timezone
from datetime import datetime

# --- List of all known date formats ---
SEEDLOG_FORMATS = [
    '%b %d %Y %H:%M:%S',      # "Sep 11 2025 03:18:54"
    '%m/%d/%Y %H:%M:%S',      # "12/16/2021 14:42:35"
]

PRESET_FORMATS = [
    '%b %d %Y %H:%M:%S',      # "Sep 11 2025 00:45:23"
    '%Y-%m-%d %H:%M:%S.%f',   # "2025-03-29 20:11:20.535182"
]

# --- Helper function to parse multiple formats ---
def parse_flexible_date(date_string, strptime_formats):
    """
    Tries to parse a date string using multiple format codes.
    It also specifically handles the ISO format with a 'T'.
    """
    # An empty or non-string value can't be parsed.
    if not isinstance(date_string, str) or not date_string.strip():
        return None

    # First, try the robust `fromisoformat` for strings with a 'T'
    if 'T' in date_string:
        try:
            return datetime.fromisoformat(date_string)
        except ValueError:
            pass # If it fails, we'll let the strptime formats try

    # Next, try all the other formats we've defined
    for fmt in strptime_formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue # If this format fails, try the next one

    # If no format matched, return None
    return None

# --- Main migration logic ---
def convert_datestrings(apps, schema_editor):
    Preset = apps.get_model('webapp', 'Preset')
    SeedLog = apps.get_model('webapp', 'SeedLog')
    
    # Use one consistent timestamp for all blank records in this run
    MIGRATION_RUN_TIME = timezone.now()
    
    print("\nConverting Preset.created_at strings to datetime...")
    presets_to_update = []
    for preset in Preset.objects.iterator():
        date_string = preset.created_at
        parsed_date = parse_flexible_date(date_string, PRESET_FORMATS)

        if parsed_date:
            # Successfully parsed a valid date string
            preset.created_at_dt = parsed_date
            presets_to_update.append(preset)
        elif not date_string or not date_string.strip():
            # The string was blank or null, so we default it
            preset.created_at_dt = MIGRATION_RUN_TIME
            presets_to_update.append(preset)
        else:
            # The string had content, but we failed to parse it.
            print(f"  - WARNING: Could not parse preset '{preset.pk}' created_at: '{date_string}'")

    if presets_to_update:
        Preset.objects.bulk_update(presets_to_update, ['created_at_dt'])
    print(f"Preset conversion complete. Updated {len(presets_to_update)} records.")

    print("\nConverting SeedLog.timestamp strings to datetime...")
    logs_to_update = []
    total_logs_processed = 0
    batch_size = 5000
    
    for log in SeedLog.objects.iterator():
        total_logs_processed += 1
        date_string = log.timestamp
        parsed_date = parse_flexible_date(date_string, SEEDLOG_FORMATS)

        if parsed_date:
            log.timestamp_dt = parsed_date
            logs_to_update.append(log)
        elif not date_string or not date_string.strip():
            log.timestamp_dt = MIGRATION_RUN_TIME
            logs_to_update.append(log)
        else:
            print(f"  - WARNING: Could not parse seedlog id {log.id} timestamp: '{date_string}'")
        
        if len(logs_to_update) >= batch_size:
            SeedLog.objects.bulk_update(logs_to_update, ['timestamp_dt'])
            print(f"  - Processed batch of {len(logs_to_update)} logs...")
            logs_to_update = []

    if logs_to_update:
        SeedLog.objects.bulk_update(logs_to_update, ['timestamp_dt'])
        print(f"  - Processed final batch of {len(logs_to_update)} logs.")

    print(f"SeedLog conversion complete. Processed {total_logs_processed} total records.")


class Migration(migrations.Migration):

    dependencies = [
        # Remember to update this to point to your PREVIOUS migration file!
        ('webapp', '0003_preset_created_at_dt_seedlog_timestamp_dt'), 
    ]

    operations = [
        migrations.RunPython(convert_datestrings, reverse_code=migrations.RunPython.noop),
    ]
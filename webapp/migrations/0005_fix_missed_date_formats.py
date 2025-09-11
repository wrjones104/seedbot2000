# in webapp/migrations/0005_fix_missed_date_formats.py

from django.db import migrations
from datetime import datetime

# The new format we missed: "1/5/2023"
NEW_SEEDLOG_FORMAT = '%m/%d/%Y'

def fix_missed_dates(apps, schema_editor):
    SeedLog = apps.get_model('webapp', 'SeedLog')

    # Find records that were missed by the previous migration.
    # These are records where the new datetime field is still empty.
    missed_logs = SeedLog.objects.filter(timestamp_dt__isnull=True)
    logs_to_update = []

    print(f"\nFound {missed_logs.count()} records with un-parsed date formats. Attempting to fix...")

    for log in missed_logs:
        if isinstance(log.timestamp, str) and log.timestamp:
            try:
                # Parse the string using the newly identified format.
                # Since this format has no time, it will default to 00:00:00.
                parsed_date = datetime.strptime(log.timestamp, NEW_SEEDLOG_FORMAT)
                log.timestamp_dt = parsed_date
                logs_to_update.append(log)
            except (ValueError, TypeError):
                # This will catch any other formats we might have still missed.
                print(f"  - WARNING: Still could not parse seedlog id {log.id} timestamp: '{log.timestamp}'")

    if logs_to_update:
        SeedLog.objects.bulk_update(logs_to_update, ['timestamp_dt'])
        print(f"Successfully fixed and updated {len(logs_to_update)} records.")
    elif missed_logs.count() > 0:
         print("Could not fix any of the remaining records with the new format.")
    else:
        print("No records needed fixing.")


class Migration(migrations.Migration):

    dependencies = [
        # This new migration runs after the main data conversion
        ('webapp', '0004_convert_string_to_datetime'),
    ]

    operations = [
        migrations.RunPython(fix_missed_dates, reverse_code=migrations.RunPython.noop),
    ]
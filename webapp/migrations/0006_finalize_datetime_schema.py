# in webapp/migrations/0006_finalize_datetime_schema.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_fix_missed_date_formats'),
    ]

    operations = [
        # Step 1: Remove the old string-based fields
        migrations.RemoveField(
            model_name='preset',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='seedlog',
            name='timestamp',
        ),
        
        # Step 2: Rename the temporary datetime fields to their final names
        migrations.RenameField(
            model_name='preset',
            old_name='created_at_dt',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='seedlog',
            old_name='timestamp_dt',
            new_name='timestamp',
        ),
    ]
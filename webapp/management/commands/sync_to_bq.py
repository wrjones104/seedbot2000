import pandas as pd
import pandas_gbq  # Corrected import
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from webapp.models import SeedLog
from google.oauth2 import service_account

class Command(BaseCommand):
    help = 'Syncs new SQLite SeedLog entries to BigQuery'

    def handle(self, *args, **kwargs):
        # Configuration - MAKE SURE TO PUT YOUR REAL PROJECT ID HERE
        project_id = '825852303491' 
        dataset_id = 'seedbot_stats'
        table_id = 'seed_logs'
        full_table_id = f"{project_id}.{dataset_id}.{table_id}"
        
        # Path to your existing JSON key
        key_path = settings.BASE_DIR / "data" / "seedbot-metrics-56ffc0ce1d4f.json"
        credentials = service_account.Credentials.from_service_account_file(key_path)

        self.stdout.write(f"[{timezone.now()}] Starting BigQuery sync...")

        # 1. Get the 'High Water Mark' (Max ID) from BigQuery
        try:
            query = f"SELECT MAX(id) as max_id FROM `{full_table_id}`"
            # Updated to use pandas_gbq.read_gbq
            max_id_df = pandas_gbq.read_gbq(query, project_id=project_id, credentials=credentials)
            last_synced_id = max_id_df['max_id'].iloc[0]
            
            if pd.isna(last_synced_id):
                last_synced_id = 0
                
            self.stdout.write(f"Last synced ID in BigQuery: {last_synced_id}")
            
        except Exception as e:
            self.stdout.write(f"Table lookup failed (assuming empty/new): {e}")
            last_synced_id = 0

        # 2. Fetch only NEW rows from SQLite
        new_seeds = SeedLog.objects.filter(id__gt=last_synced_id).order_by('id')
        
        data = list(new_seeds.values(
            'id', 'creator_id', 'creator_name', 'seed_type', 'share_url', 
            'timestamp', 'server_name', 'server_id', 'channel_name', 
            'channel_id', 'random_sprites', 'hash', 'seed'
        ))

        if not data:
            self.stdout.write("No new rows to sync.")
            return

        df = pd.DataFrame(data)

        # 3. Clean/Format Data
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])

        self.stdout.write(f"Uploading {len(df)} new rows to BigQuery...")

        # 4. Push to BigQuery
        # Updated to use pandas_gbq.to_gbq
        pandas_gbq.to_gbq(
            df,
            destination_table=f"{dataset_id}.{table_id}",
            project_id=project_id,
            if_exists='append',
            credentials=credentials
        )

        self.stdout.write(self.style.SUCCESS(f"Successfully synced {len(df)} rows."))
import pygsheets
from django.conf import settings

def write_to_gsheets(metrics_data):
    """Writes a row of data to the SeedBot Metrics Google Sheet."""
    try:
        # This path assumes the service file is in the 'db' folder of the adjacent project
        keyfile_path = settings.BASE_DIR.parent / 'seedbot2000' / 'db' / 'seedbot-metrics-56ffc0ce1d4f.json'
        gc = pygsheets.authorize(service_file=str(keyfile_path))
        sh = gc.open('SeedBot Metrics')
        wks = sh[0]
        
        # Prepare values in the correct order for the sheet
        values_to_insert = [
            metrics_data.get('creator_id'),
            metrics_data.get('creator_name'),
            metrics_data.get('seed_type'),
            metrics_data.get('random_sprites', 'N/A'),
            metrics_data.get('share_url'),
            metrics_data.get('timestamp'),
            metrics_data.get('server_name', 'WebApp'),
            metrics_data.get('server_id', 'N/A'),
            metrics_data.get('channel_name', 'N/A'),
            metrics_data.get('channel_id', 'N/A'),
        ]
        
        wks.append_table(values=values_to_insert, start='A1', end=None, dimension='ROWS', overwrite=False)
        print("Successfully wrote to Google Sheet.")
    except Exception as e:
        print(f'Unable to write to gsheets because of:\n{e}')
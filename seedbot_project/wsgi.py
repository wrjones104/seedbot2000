import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv # <--- Add this import

# Point to the base directory where your .env file is located
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the .env file
load_dotenv(os.path.join(BASE_DIR, '.env')) # <--- Add this line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seedbot_project.settings')

application = get_wsgi_application()
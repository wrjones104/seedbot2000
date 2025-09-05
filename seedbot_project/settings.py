import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY')
WC_API_KEY = os.getenv('new_api_key')
DEV_API_KEY = os.getenv('dev_api_key')
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
ENV_TYPE = os.getenv('ENVIRONMENT', 'dev')

DEBUG = ENV_TYPE != 'prod'
ALLOWED_HOSTS = ['seedbot.net', 'www.seedbot.net'] if ENV_TYPE == 'prod' else ['*']

INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'django.contrib.sites', 'django.contrib.redirects', 'allauth', 'allauth.account',
    'allauth.socialaccount', 'allauth.socialaccount.providers.discord', 'webapp', 'bot',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 'allauth.account.middleware.AccountMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]
ROOT_URLCONF = 'seedbot_project.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'seedbot_project.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'seeDBot.sqlite',
        'OPTIONS': {
            'check_same_thread': False,
        }
    }
}
AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}, {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ = 'en-us', 'UTC', True, True
STATIC_URL, STATICFILES_DIRS, STATIC_ROOT = 'static/', [BASE_DIR / "static"], BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "data" / "seeds" if ENV_TYPE == 'prod' else BASE_DIR / "data" / "seeds"
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend', 'allauth.account.auth_backends.AuthenticationBackend']
SITE_ID, LOGIN_REDIRECT_URL, DEFAULT_AUTO_FIELD = 1, '/', 'django.db.models.BigAutoField'
SOCIALACCOUNT_PROVIDERS = {'discord': {'SCOPE': ['identify', 'email'], 'AUTH_PARAMS': {'access_type': 'online'}}}
SOCIALACCOUNT_AUTO_SIGNUP, ACCOUNT_EMAIL_VERIFICATION, SOCIALACCOUNT_LOGIN_ON_GET, ACCOUNT_LOGOUT_ON_GET = True, "none", True, True
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'bot': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'webapp': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        }
    },
}
import os
import sys
from pathlib import Path
import environ

# Path & Environment setup
BASE_DIR = Path(__file__).resolve().parent.parent
TESTING = sys.argv[1:2] == ['test'] or "pytest" in sys.modules

env = environ.Env(DEBUG=(bool, False),
                  DJANGO_SECRET=(str, None),
                  DB_NAME=(str, 'postgres'),
                  DB_USER=(str, 'postgres'),
                  DB_PASSWORD=(str, 'postgres'),
                  DB_HOST=(str, 'localhost'),
                  DB_PORT=(int, 5432),
                  PG_SERVICE=(str, None),
                  PG_PASS=(str, None))

env.read_env(os.path.join(BASE_DIR, ".env"))

# Secret management
SECRET_KEY = os.getenv('DJANGO_SECRET')

if not SECRET_KEY:  # Generate the secret key if not present
    from django.core.management.utils import get_random_secret_key

    SECRET_KEY = get_random_secret_key()

    with open(os.path.join(BASE_DIR, ".env"), "a+") as env_file:
        env_file.write(f"\nDJANGO_SECRET={SECRET_KEY}\n")

DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mapsearch.user'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

db_data = dict(ENGINE='django.db.backends.postgresql')
if all([env(x) for x in ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']]):
    db_data['NAME'] = env('DB_NAME')
    db_data['USER'] = env('DB_USER')
    db_data['PASSWORD'] = env('DB_PASSWORD')
    db_data['HOST'] = env('DB_HOST')
    db_data['PORT'] = env('DB_PORT')

elif all([env(x) for x in ['PG_SERVICE', 'PG_PASS']]):
    db_data['OPTIONS'] = dict(service=env('PG_SERVICE'), passfile=env('PG_PASS'))

else:
    raise ValueError('Missing DB credentials')

DATABASES = {'default': db_data}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

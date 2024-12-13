from pathlib import Path
from decouple import config
import os

# openAI API key
OPENAI_API_KEY = config("OPENAI_API_KEY", cast=str, default="")
OPENAI_API_ENDPOINT = config("OPENAI_API_ENDPOINT", cast=str, default="")
OPENAI_API_BASE = config("OPENAI_API_BASE", cast=str, default="")

DI_API_KEY = config("DI_API_KEY", cast=str, default="")
DI_API_ENDPOINT = config("DI_API_ENDPOINT", cast=str, default="")

# azure storage blob connection
BLOB_CONNECTION_STR = config("BLOB_CONNECTION_STR", cast=str, default="")
BLOB_CONTAINER_NAME = config("BLOB_CONTAINER_NAME", cast=str, default="")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q)$o6(8h1d_5+pl6$il0th#rm2ax76w=qg8^cq_!efl%436gi0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    'https://dfo-openai.azurewebsites.net',
    'https://pssi-openai-analyzer-dev.dfo-sc2g-dev-ase01.appserviceenvironment.net',
    'https://127.0.0.1',
    'https://pssi-openai-analyzer-prd-01.dfo-sc2g-prob-ase01.appserviceenvironment.net'
]

ALLOWED_HOSTS = [
     'dfo-openai.azurewebsites.net',
     'pssi-openai-analyzer-dev.dfo-sc2g-dev-ase01.appserviceenvironment.net',
     '127.0.0.1',
     'pssi-openai-analyzer-prd-01.dfo-sc2g-prob-ase01.appserviceenvironment.net'
]
CORS_ORIGIN_WHITELIST = [
    'dfo-openai.azurewebsites.net',
    'pssi-openai-analyzer-dev.dfo-sc2g-dev-ase01.appserviceenvironment.net',
    '127.0.0.1',
    'pssi-openai-analyzer-prd-01.dfo-sc2g-prob-ase01.appserviceenvironment.net'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'combined_openAI_app',
    'demo',
    'bootstrap4',
    'chatbot'
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

ROOT_URLCONF = 'combined_openAI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'combined_openAI.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

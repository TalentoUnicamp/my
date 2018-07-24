"""Django settings for project project.

Generated by 'django-admin startproject' using Django 2.0

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Website root url
ROOT_URL = os.environ.get('ROOT_URL', 'localhost:8000')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET', 'abc123')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = eval(os.environ.get('DEBUG', 'False').capitalize())

# manage.py test mode that disables fb connection stuff
TEST_MODE = eval(os.environ.get('TEST_MODE', 'False').capitalize())

ALLOWED_HOSTS = eval(os.environ.get('ALLOWED_HOSTS', '[]'))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'debug_panel',
    'compressor',
    'compressor_toolkit',
    'storages',

    'rest_framework',

    'django_extensions',

    'channels',
    'model_sockets',

    'dashboard',
    'user_profile',
    'social',
    'hacker',
    'staff',
    'settings',
    'application',
    'godmode',
    'company',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_panel.middleware.DebugPanelMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Project urls
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
FILE_UPLOAD_HANDLERS = ['django.core.files.uploadhandler.TemporaryFileUploadHandler']
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS Storage settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False


# Compressor settings
COMPRESS_OFFLINE = not DEBUG

COMPRESS_PRECOMPILERS = (
    ('module', 'compressor_toolkit.precompilers.ES6Compiler'),
    ('text/x-scss', 'compressor_toolkit.precompilers.SCSSCompiler'),
    ('text/less', 'lessc {infile} {outfile}'),
)

COMPRESS_ES6_COMPILER_CMD = (
    'export NODE_PATH="{paths}" && '
    '{browserify_bin} "{infile}" -o "{outfile}" '
    '-t [ envify --NODE_ENV production ] '
    '-t [ "{node_modules}/babelify" --presets="{node_modules}/babel-preset-es2015" ] '
)
if not DEBUG:
    COMPRESS_ES6_COMPILER_CMD = COMPRESS_ES6_COMPILER_CMD.replace("{browserify_bin}", "NODE_ENV=production {browserify_bin} -g envify")

COMPRESS_URL = 'https://{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)
COMPRESS_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Celery stuff
CELERY_BROKER_URL = os.environ.get('REDIS_URL')

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_CONTACT_EMAIL = os.environ.get('EMAIL_ACCOUNT')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_ACCOUNT')
EMAIL_HOST_USER = os.environ.get('EMAIL_ACCOUNT')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_USE_TLS = eval(os.environ.get('EMAIL_USE_TLS', 'True'))
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
SERVER_EMAIL = os.environ.get('EMAIL_ACCOUNT')

ADMINS = [('Admin', os.environ.get('ADMIN_ACCOUNT')), ]


# Event data
EVENT_NAME = os.environ.get('EVENT_NAME', 'Hackathon')


# Model Sockets settings
# Name of the app containing the self model
MSOCKS_SELF_APP = 'user_profile'
# Name of the self Model
MSOCKS_SELF_MODEL = 'Profile'
MSOCK_AUTH_USER_RELATION_ID = 'user.profile.id'
MSOCKS_SELF_SUBSCRIPTION_FIELDS = [
    'unique_id',
    'state',
    'is_hacker',
    'is_staff',
    'is_admin',
    'is_employee',
    'token',
    'is_verified',
    'full_name',
    'email',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: eval(os.environ.get('SHOW_TOOLBAR_CALLBACK', 'True'))  # disables it
    # '...
}

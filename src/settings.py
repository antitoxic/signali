"""
Django settings for config project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/

For deployments see https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import dotenv
from getenv import env

from django.utils.translation import ugettext_lazy as _

#################### Environment-specific #################
# important directories
PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
ENV_ROOT = os.path.realpath(os.path.join(PROJECT_ROOT, 'env'))
THEMES_ROOT = os.path.realpath(env('THEMES_ROOT', os.path.join(PROJECT_ROOT, 'themes')))

# add src dir to include path
sys.path.append(os.path.join(PROJECT_ROOT, "src"))

# load .env file if existing
PROJECT_ENV_FILE = env('PROJECT_ENV_FILE', os.path.join(ENV_ROOT, '.django'))
if os.path.isfile(PROJECT_ENV_FILE):
    dotenv.load_dotenv(PROJECT_ENV_FILE)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

WSGI_APPLICATION = 'env.wsgi.application'


################### Project-specific ###################

# Application definition
INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'redactor',
    'rating',
    'contact',
    'taxonomy',
    'siteguide',
    'django_select2',
    'restful',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'restful.middleware.HttpMergeParameters',
    'restful.middleware.HttpMethodOverride',
    'restful.middleware.ResponseFormatDetection',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'restful.error_handler.ErrorHandler',
    'restful.middleware.TemplateExtensionByAcceptedType',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
    "django.core.context_processors.csrf",
)

THEME = 'default'
# register theme files
THEME_DIR = os.path.join(THEMES_ROOT, THEME)
if not os.path.isdir(THEME_DIR):
    raise Exception('Improperly configured theme')
TEMPLATE_DIRS = (os.path.join(THEME_DIR ,'templates'),)
STATICFILES_DIRS = [os.path.join(THEME_DIR, 'build'), os.path.join(THEME_DIR),]

ROOT_URLCONF = 'urls'

# http://stackoverflow.com/a/111032/339872
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASS'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'bg'
TIME_ZONE = 'Europe/Sofia'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files / Asset files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "upload")
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

# Third-party packages options
REDACTOR_OPTIONS = {
    'lang': 'bg',
    'buttons': ['formatting', 'bold', 'italic','unorderedlist', 'orderedlist','image', 'link'],
    'formatting': ['p', 'h4', 'h3', 'h2', 'h1']
}
REDACTOR_UPLOAD = "redactor/"


SUIT_CONFIG = {
  'SEARCH_URL': '',
  'ADMIN_NAME': 'Signali.bg',
  'MENU': (
    {
      'label': _('Contact points'),
      'icon': 'icon-star',
      'models': (
          {'model': 'contact.contactpoint', 'label': _('Contact points')},
          {'model': 'contact.organisation', 'label': _('Organisations')},
          {'model': 'contact.contactpointrequirement', 'label': _('Contact point requirements')},
      )
    },
    {
      'label': _('System'),
      'icon': 'icon-barcode',
      'models': (
          {'model': 'siteguide.setting', 'label': _('Settings')},
      )
    },
  )
}
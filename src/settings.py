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
LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'src/locale'),
)

# load .env file if existing
PROJECT_ENV_FILE = env('PROJECT_ENV_FILE', os.path.join(ENV_ROOT, '.django'))
if os.path.isfile(PROJECT_ENV_FILE):
    dotenv.load_dotenv(PROJECT_ENV_FILE)

# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG', False)

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['.signali.bg']

WSGI_APPLICATION = 'env.wsgi.application'


################### Project-specific ###################


AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GooglePlusAuth',
    'social.backends.open_id.OpenIdAuth',
    'social.backends.email.EmailAuth',
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    # backend tries to retrieve details from the incoming user data
    'social.pipeline.social_auth.social_details',
    # backend tries to get id be used with social user object
    'social.pipeline.social_auth.social_uid',
    # check if auth is allowed for the provided user details
    'social.pipeline.social_auth.auth_allowed',
    # retrieves user ONLY if the user is registered with the current backend and have UserSocialAuth record
    # Important note: users created outside social pipeline most likely don't have UserSocialAuth
    # example for common error scenario: manage.py createsuperadmin
    'social.pipeline.social_auth.social_user',
    # retrieve user if there was no match by social_user
    'security.pipeline.local_user',
    # extracts possible username for backends that might need it
    'social.pipeline.user.get_username',
    # throws error if user exists and the incoming data states the user is trying to register
    'security.pipeline.prevent_duplicate_on_register',
    # throws error if user does not exist and the incoming data states the user is trying to login
    'security.pipeline.refuse_missing_user_on_login',
    # checks user password against the incoming password from the request
    'security.pipeline.user_password',
    # uncomment the following and the other "checkpoint" pipeline entries
    # to present the user with an option to doublecheck details provided by social auth upon registration
    # 'user.pipeline.signupcheckpoint',
    # validates user data and update `details` keyword argument
    'user.pipeline.parse_user_data',
    'security.pipeline.create_user',
    'security.pipeline.save_password',
    'social.pipeline.social_auth.associate_user', # creates a social user record
    'social.pipeline.social_auth.load_extra_data', # adds provider metadata like "expire" or "id"
    'security.pipeline.user_details', # tops up User model fields with what's available in "details" parameter
    # sends out mail validation for new users
    'security.pipeline.send_email_validation',
)
LOGIN_URL = '/user/join/'
LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.profile'
]
SOCIAL_AUTH_URL_NAMESPACE = 'security'
SOCIAL_AUTH_FORM_URL = '/user/join/'
SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'user.utils.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/security/email-validation/sent/'

SOCIAL_AUTH_FACEBOOK_KEY = '1623717401196966'
SOCIAL_AUTH_FACEBOOK_SECRET = env("SOCIAL_AUTH_FACEBOOK_SECRET")
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'bg_BG'}
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']


EMAIL_CONNECTIONS = {
    'internal': {
        'host': env('EMAIL_CONNECTION_INTERNAL_HOST'),
        'username':  env('EMAIL_CONNECTION_INTERNAL_USER'),
        'password':  env('EMAIL_CONNECTION_INTERNAL_PASS'),
        'port':  env('EMAIL_CONNECTION_INTERNAL_PORT'),
        'use_tls': env('EMAIL_CONNECTION_INTERNAL_TLS'),
    },
    'public': {
        'host': env('EMAIL_CONNECTION_PUBLIC_HOST'),
        'username':  env('EMAIL_CONNECTION_PUBLIC_USER'),
        'password':  env('EMAIL_CONNECTION_PUBLIC_PASS'),
        'port':  env('EMAIL_CONNECTION_PUBLIC_PORT'),
        'use_tls': env('EMAIL_CONNECTION_PUBLIC_TLS'),
    },
}

DEFAULT_FROM_EMAIL = 'info@signali.bg'
ADMIN_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_CONNECTION_LABEL_INTERNAL = 'internal'
EMAIL_CONNECTION_LABEL_PUBLIC = 'public'
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = EMAIL_CONNECTIONS['internal']["host"]
EMAIL_HOST_USER = EMAIL_CONNECTIONS['internal']["username"]
EMAIL_HOST_PASSWORD = EMAIL_CONNECTIONS['internal']["password"]
EMAIL_PORT = EMAIL_CONNECTIONS['internal']["port"]
EMAIL_USE_TLS = EMAIL_CONNECTIONS['internal']["use_tls"]

THEME = 'default'
# register theme files
THEME_DIR = os.path.join(THEMES_ROOT, THEME)
THEME_STATIC_DIR = os.path.join(THEME_DIR, 'build')
if not os.path.isdir(THEME_DIR):
    raise Exception('Improperly configured theme')
TEMPLATE_DIRS = (os.path.join(THEME_DIR, 'templates'),)
STATICFILES_DIRS = [THEME_STATIC_DIR,]

# Application definition
INSTALLED_APPS = (
    'suit',
    'signali.apps.SignaliAdminConfig',
    'adminextra',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'redactor',
    'rules.apps.AutodiscoverRulesConfig',
    'django_select2',
    'sorl.thumbnail',
    'restful',
    'notification',
    'signali_notification.apps.NotificationConfig',
    'security.apps.SecurityConfig',
    'user',
    'location',
    'taxonomy',
    'accessibility',
    'signali_contact.apps.ContactConfig',
    'signali_contact.apps.FeedbackConfig',
    'signali_contact',
    'signali_accessibility',
    'signali_location',
    'signali_taxonomy',
    'signali',
    'themes.'+THEME+'.widgets',
    'django_bootstrap_datetimepicker',
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
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.core.context_processors.request',
    "django.core.context_processors.csrf",
)

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
AUTH_USER_MODEL = 'user.User'


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

CONTACT_USER_CRITERIA_FORM = 'signali_contact.forms.UserCriteriaForm'
CONTACT_POINT_FORM = 'signali_contact.forms.ContactPointForm'

CONTACT_POINT_MODEL = 'signali_contact.ContactPoint'
CONTACT_ORGANISATION_MODEL = 'signali_contact.Organisation'
CONTACT_KEYWORD_MODEL = 'signali_taxonomy.Keyword'
CONTACT_CATEGORY_MODEL = 'signali_taxonomy.Category'
CONTACT_AREA_MODEL = 'signali_location.Area'
CONTACT_FEEDBACK_MODEL = 'signali_contact.SignalContactPointFeedback'

ACCESSIBILITY_PAGE_MODEL = 'signali_accessibility.Page'

THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_QUALITY = 100
THUMBNAIL_REDIS_HOST = env('REDIS_HOST')
THUMBNAIL_REDIS_PORT = env('REDIS_PORT')
THUMBNAIL_REDIS_DB = env('REDIS_CACHE_DB')

CACHEOPS_REDIS = {
    'host': env('REDIS_HOST'),
    'port': env('REDIS_PORT'),
    'db': env('REDIS_CACHE_DB')
}
CACHEOPS = {}

# If you are developing without access to images, please refer to:
# http://sorl-thumbnail.readthedocs.org/en/latest/reference/settings.html#thumbnail-dummy

# Admin menu config
SUIT_CONFIG = {
    'SEARCH_URL': '',
    'ADMIN_NAME': 'signali.bg',
    'MENU': (
        {
            'label': _('main content'),
            'icon': 'icon-star',
            'models': (
                {'model': 'signali_contact.contactpoint', 'label': _('contact points')},
                {'model': 'signali_contact.organisation', 'label': _('organisations')},
                {'model': 'signali_accessibility.page', 'label': _('pages')},
                {'model': 'signali_location.area', 'label': _('areas')},
            )
        },
        {
            'label': _('users'),
            'icon': 'icon-user',
            'models': (
                {'model': AUTH_USER_MODEL.lower(), 'label': _('registered')},
                {'model': 'signali_notification.subscriber', 'label': _('subscribers')},
            )
        },
        {
            'label': _('taxonomy'),
            'icon': 'icon-tags',
            'models': (
                {'model': 'signali_taxonomy.category', 'label': _('categories')},
                {'model': 'signali_taxonomy.keyword', 'label': _('keywords')},
            )
        },
        {
            'label': _('settings'),
            'icon': 'icon-cog',
            'models': (
                {'model': 'signali.setting', 'label': _('settings')},
                {'model': 'signali_location.areasize', 'label': _('areas sizes')},
            )
        },
        {
            'label': _('troubleshoot'),
            'icon': 'icon-barcode',
            'models': (
                {'model': 'default.association', 'label': _('user associations')},
                {'model': 'default.nonce', 'label': _('user nonce records')},
                {'model': 'default.usersocialauth', 'label': _('user social auth')},
                {'model': 'auth.group', 'label': _('user groups')},
            )
        },
    )
}

PUBLIC_SETTINGS = ['SOCIAL_AUTH_FACEBOOK_KEY', 'SOCIAL_AUTH_FACEBOOK_SCOPE']
CLASS_SETTINGS = [
    'CONTACT_USER_CRITERIA_FORM',
    'CONTACT_POINT_FORM',
    'CONTACT_FEEDBACK_FORM',
]
MODEL_SETTINGS = [
    'CONTACT_POINT_MODEL',
    'CONTACT_ORGANISATION_MODEL',
    'CONTACT_KEYWORD_MODEL',
    'CONTACT_CATEGORY_MODEL',
    'CONTACT_AREA_MODEL',
    'CONTACT_FEEDBACK_MODEL',
]

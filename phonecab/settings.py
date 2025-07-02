"""
Django settings for Phonecab 3 project.

"""
from unipath import Path
import os

PROJECT_DIR = Path(__file__).ancestor(2)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Ubuntu installation need sudo to prefix root commands. Centos one do not.
USE_SUDO = False

ADMINS = (
    ('Admin', 'admin@example.com'),
)

MANAGERS = ADMINS

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': PROJECT_DIR.child('db.sqlite3'),
#     }
# }

# Mysql settings
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.getenv('DB_NAME', 'phonecab'),
        'USER': os.getenv('DB_USER', 'phonecab'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'phonecab'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}

ALLOWED_HOSTS = ['*', '127.0.0.1']


# APP SETTINGS
# Numero elementi per pagina
ITEMS_PER_PAGE = 5

# percorso file audio
RECORDS_ROOT = '/var/spool/asterisk/monitor'
TMP_ZIP_ROOT = '/tmp/'

FILESYSTEM = '/dev/sda1'
EXT_FILESYSTEM = '/dev/sdb1'

# Chiusura sessione alla chiusura del browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TIME_ZONE = 'Europe/Rome'

LANGUAGE_CODE = 'it-it'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = False

MEDIA_ROOT = ''

MEDIA_URL = ''

LOGIN_URL = '/login'


STATIC_ROOT = '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    PROJECT_DIR.child("static"),
    #os.path.join(CURRENT_DIR, "static"),
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'dr-a*1et&hso645hjua&0(plo6v=cpn9ve3gerdg9ydmpk0hxt'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'phonecab.urls'

WSGI_APPLICATION = 'phonecab.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_DIR.child("templates")],
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

# Keep the old setting for backwards compatibility with very old Django

TEMPLATE_DIRS = [
    PROJECT_DIR.child("templates"),
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    # 'django_extensions',
    'phoneusers',
    'acls',
    'cdrs',
    'records',
    'audits',
    'prefs',
    'archives',
    'logs',
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


TEST_RUNNER = 'django.test.runner.DiscoverRunner'


try:
    from settings_local import *
except:
    pass

# -*- coding: utf-8 -*-
# Django settings for focus project.

import os.path

BASE_PATH = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SERVER_EMAIL = 'fredrik+django@fncit.no'

ADMINS = (
(u'Fredrik Nygård Carlsen', 'fredrik@fncit.no'),
)

MANAGERS = ADMINS

import socket

if socket.gethostname().startswith('FREDRIK'):
    LIVEHOST = False
else:
    LIVEHOST = True

if LIVEHOST:
    DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = 'frecarlsen_focus'             # Or path to database file if using sqlite3.
    DATABASE_USER = 'frecarlsen'             # Not used with sqlite3.
    DATABASE_PASSWORD = 'XDuGEMac'         # Not used with sqlite3.
    DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
else:
    DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = 'focusDB'             # Or path to database file if using sqlite3.
    DATABASE_USER = ''             # Not used with sqlite3.
    DATABASE_PASSWORD = ''         # Not used with sqlite3.
    DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'Europe/Oslo'

LANGUAGE_CODE = 'no-nb'

SITE_ID = 1

SITE_URL = "http://focus.fncit.no"

USE_I18N = True

MEDIA_ROOT = BASE_PATH + '/media'

LOGIN_URL = "/accounts/login"

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = '$cv2_y@eqne&amp;%cp2fs!8@#p#*!q)9etm!++#34f01^mlnk6=et'

TEMPLATE_LOADERS = (
'django.template.loaders.filesystem.load_template_source',
'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
'django.middleware.common.CommonMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.locale.LocaleMiddleware',
'django.middleware.doc.XViewMiddleware',

'core.middleware.AuthenticationMiddleware',
'core.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'focus.urls'

TEMPLATE_DIRS = (
BASE_PATH + '/templates/',
)

INSTALLED_APPS = (
'django.contrib.contenttypes',
'django.contrib.sessions',

'app.admin',

#All the applicaitons
'core',
'app.company',
'app.announcements',
'app.accounts',
'app.customers',
'app.projects',
'app.orders',
'app.hourregistrations',
'app.contacts',
'app.files',
'app.dashboard',
'app.stock',
'app.suppliers',
'app.search',

#Other
'south',
)

TEMPLATE_CONTEXT_PROCESSORS = (
'django.core.context_processors.request',
'django.core.context_processors.i18n',
'core.context_processors.message',
'core.context_processors.user',
)
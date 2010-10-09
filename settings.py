# -*- coding: utf-8 -*-
# Django settings for focus project.

import os.path

BASE_PATH = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG




SERVER_EMAIL = 'fredrik@fncit.no'

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
    DATABASE_ENGINE     = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME       = 'frecarlsen_focus'             # Or path to database file if using sqlite3.
    DATABASE_USER       = 'frecarlsen'             # Not used with sqlite3.
    DATABASE_PASSWORD   = 'XDuGEMac'         # Not used with sqlite3.
    DATABASE_HOST       = ''             # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT       = ''             # Set to empty string for default. Not used with sqlite3.
else:    
    DATABASE_ENGINE     = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME       = 'focusDB'             # Or path to database file if using sqlite3.
    DATABASE_USER       = ''             # Not used with sqlite3.
    DATABASE_PASSWORD   = ''         # Not used with sqlite3.
    DATABASE_HOST       = ''             # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT       = ''             # Set to empty string for default. Not used with sqlite3.


AUTH_PROFILE_MODULE = 'core.UserProfile'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Oslo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'no-nb'

SITE_ID = 1

SITE_URL = "http://focus.fncit.no/"

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'core.backend.ObjectPermBackend',
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = BASE_PATH+'/media'

LOGIN_URL = "/accounts/login"
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$cv2_y@eqne&amp;%cp2fs!8@#p#*!q)9etm!++#34f01^mlnk6=et'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#   'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    
    #reversion
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',

    #For getting current user
    'core.middleware.ThreadLocals',
)

ROOT_URLCONF = 'focus.urls'


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    BASE_PATH+'/templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.messages',

    #Admin-for leaders
    'app.admin',
    
    #All the applicaitons
    'core',  
    'app.announcements',
    'app.bugreporting',
    'app.timetracking',
    'app.accounts',
    'app.customers',
    'app.projects',
    'app.orders',
    'app.contacts',
    'app.internalmessages',
    'app.tickets',
    'app.dashboard',
    
    #Other    
    'south',    
    'reversion',
)

TEMPLATE_CONTEXT_PROCESSORS = (
                               'django.core.context_processors.request',
                               'django.contrib.auth.context_processors.auth',
                               'django.contrib.messages.context_processors.messages',
)

# Override the server-derived value of SCRIPT_NAME 
# See http://code.djangoproject.com/wiki/BackwardsIncompatibleChanges#lighttpdfastcgiandothers
FORCE_SCRIPT_NAME = ''

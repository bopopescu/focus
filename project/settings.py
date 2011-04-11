# -*- coding: utf-8 -*-

import os.path

BASE_PATH = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SERVER_EMAIL = 'fredrik+django@fncit.no'
NO_REPLY_EMAIL = 'no-reply@focustime.no'
DEBUG_EMAIL = "fredrik+debug@fncit.no"

ADMINS = (
(u'Fredrik Nygård Carlsen', 'fredrik@fncit.no'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'project.db'
    }
}

TIME_ZONE = 'Europe/Oslo'
DATE_FORMAT = 'd.m.Y'
TIME_FORMAT = 'H.i'

LANGUAGE_CODE = 'en'

_ = lambda s: s

LANGUAGES = (
('en', _('English')),
('nb', _('Norwegian')),
)

SITE_ID = 1
SITE_URL = "http://focus.fncit.no"

USE_I18N = True

LOGIN_URL = "/accounts/login/"

FORCE_SCRIPT_NAME = ""

STATIC_ROOT = BASE_PATH + '/static_media/'
STATIC_URL = '/static/'

SECRET_KEY = '$cv2_y@eqne&amp;%cp2fs!8@#p#*!q)9etm!++#34f01^mlnk6=et'

TEMPLATE_LOADERS = (
'django.template.loaders.filesystem.Loader',
'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.locale.LocaleMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.doc.XViewMiddleware',

'core.middleware.AuthenticationMiddleware',
'core.middleware.MessageMiddleware',
'core.middleware.SessionBasedLocaleMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
BASE_PATH + '/templates/',
)

STATICFILES_DIRS = (
BASE_PATH + '/files/media/',
)

INTERNAL_IPS = ('127.0.0.1')

INSTALLED_APPS = (

#Django stuff
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.staticfiles',

#Core
'core.auth.user',
'core.auth.group',
'core.auth.company',
'core.auth.log',
'core.auth.permission',
'core',

#Apps
'app.admin',
'app.company',
'app.announcements',
'app.contacts',
'app.accounts',
'app.customers',
'app.projects',
'app.files',
'app.dashboard',
'app.stock',
'app.orders',
'app.hourregistrations',
'app.suppliers',
'app.search',
'app.mail',
'app.tickets',
'app.migratefocus',

#Other
'south',
)

TEMPLATE_CONTEXT_PROCESSORS = (
'django.core.context_processors.request',
'django.core.context_processors.csrf',
'django.core.context_processors.i18n',
'django.core.context_processors.static',
'django.core.context_processors.debug',
'core.context_processors.message',
'core.context_processors.user',
)

TEST_RUNNER = 'core.tests.FocusTestSuiteRunner'
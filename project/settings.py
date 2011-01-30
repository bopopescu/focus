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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'project.db'
    }
}

TIME_ZONE = 'Europe/Oslo'
DATE_FORMAT = 'd.m.Y'
TIME_FORMAT = 'H.i'

LANGUAGE_CODE = 'no-nb'

SITE_ID = 1

SITE_URL = "http://focus.fncit.no"

USE_I18N = True

MEDIA_ROOT = BASE_PATH + '/media'

LOGIN_URL = "/accounts/login"

FORCE_SCRIPT_NAME = ""

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = '$cv2_y@eqne&amp;%cp2fs!8@#p#*!q)9etm!++#34f01^mlnk6=et'

TEMPLATE_LOADERS = (
'django.template.loaders.filesystem.Loader',
'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
'django.middleware.common.CommonMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.locale.LocaleMiddleware',
'django.middleware.doc.XViewMiddleware',

'core.middleware.AuthenticationMiddleware',
'core.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEST_RUNNER = 'core.tests.FocusTestSuiteRunner'

TEMPLATE_DIRS = (
BASE_PATH + '/templates/',
)

INSTALLED_APPS = (
'django.contrib.contenttypes',
'django.contrib.sessions',


#All the applicaitons
'core',
'app.admin',
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
'app.mail',

#Other
'south',
)

TEMPLATE_CONTEXT_PROCESSORS = (
'django.core.context_processors.request',
'django.core.context_processors.i18n',
'core.context_processors.message',
'core.context_processors.user',
)
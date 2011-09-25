from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SEND_BROKEN_LINK_EMAILS = True

import os

f = open('/home/ubuntu/passwords/db-focus.txt', 'rb')
DB_PASSWORD = f.readline().strip()
f.close()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'focus_prod',
        'USER': 'root',
        'PASSWORD': DB_PASSWORD,
    }
}

STATIC_URL = '/static/'

SITE_URL = "http://www.focustime.no"
CLIENT_LOGIN_SITE = "http://www.focustime.no/client/"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

DEBUG_EMAIL = "fredrik@fncit.no"
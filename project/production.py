from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

import os

f = open('/home/ubuntu/passwords/db-focus.txt', 'rb')
DB_PASSWORD = f.readline().strip()
f.close()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'focus',
        'USER': 'focus',
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

#EMAIL DEBUG
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'focustimeno@gmail.com'
EMAIL_HOST_PASSWORD = '4th56y44g'
EMAIL_PORT = 587

DEBUG_EMAIL = "fredrik@fncit.no"
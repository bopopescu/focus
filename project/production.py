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
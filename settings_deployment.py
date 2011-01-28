from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'frecarlsen_focus',
        'USER':'frecarlsen',
        'PASSWORD':'XDuGEMac',
    }
}

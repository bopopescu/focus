from settings import *

DEBUG = True
TEMPLATE_DEBUG = True


#EMAIL DEBUG
DEBUG_EMAIL = "focustimeno@gmail.com"
EMAIL_DEBUG_SETTINGS = {
    'EMAIL_HOST':'smtp.gmail.com',
    'EMAIL_HOST_USER':'USER@YOUR_DOMAIN.com',
    'EMAIL_HOST_PASSWORD':'YOUR_PASS',
    'EMAIL_PORT':'587',
    'EMAIL_USE_TLS': True,
}

if DEBUG:
    from utils import BogusSMTPConnection
    from django.core import mail
    mail.SMTPConnection = BogusSMTPConnection
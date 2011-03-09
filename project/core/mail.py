from django.core.mail import send_mail as django_send_mail
from django.core.mail import send_mass_mail as django_send_mall_email
from django.conf import settings

def send_mail(subject, message, fromMail, toMails, fail_silently = False):

    if settings.DEBUG:
        mail = django_send_mail(subject, message, fromMail, toMails, fail_silently=fail_silently)
        print mail
    else:
        django_send_mail(subject, message, fromMail, toMails, fail_silently=fail_silently)
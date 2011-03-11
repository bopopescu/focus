from django.core.mail import send_mail as django_send_mail
from django.core.mail import send_mass_mail as django_send_mall_email
from django.conf import settings

def send_mail(subject, message, fromMail, toMails, fail_silently = False):
    print toMails
    if settings.DEBUG:
        subject = "[debug] subject: %s" % subject
        message = "from: %s, to: %s\n\n%s" % (fromMail,toMails,message)
        mail = django_send_mail(subject, message, fromMail, [settings.DEBUG_EMAIL], fail_silently=fail_silently)
    else:
        subject = "[debug] subject: %s" % subject
        message = "from: %s, to: %s\n\n%s" % (fromMail,toMails,message)
        mail = django_send_mail(subject, message, fromMail, [settings.DEBUG_EMAIL], fail_silently=fail_silently)

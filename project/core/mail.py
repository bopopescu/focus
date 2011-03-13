from django.core.mail import send_mail as django_send_mail
from django.core.mail import send_mass_mail as django_send_mall_email
from django.conf import settings

def send_mail(subject, message, fromMail, toMails, fail_silently=False):

    recipients = []
    recipients.extend(toMails)

    #Always send debug email
    subject = "[debug] subject: %s" % subject
    message = "from: %s, to: %s\n\n%s" % (fromMail, recipients, message)
    mail = django_send_mail(subject, message, fromMail, [settings.DEBUG_EMAIL], fail_silently=fail_silently)

    #Send actual email if not in debug mode
    if not settings.DEBUG:
        mail = django_send_mail(subject, message, fromMail, recipients, fail_silently=fail_silently)
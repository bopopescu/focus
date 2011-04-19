from django.core.mail import send_mail as django_send_mail
from django.conf import settings

def send_mail(subject, message, fromMail, toMails, fail_silently=False):
    recipients = []
    recipients.extend(toMails)

    #Always send debug email
    debug_subject = "[debug] subject: %s" % subject
    debug_message = "from: %s, to: %s\n\n%s" % (fromMail, recipients, message)
    mail = django_send_mail(debug_subject, debug_message, fromMail, [settings.DEBUG_EMAIL], fail_silently=fail_silently)

    #Clean recipient list for non-emails
    for email in recipients:
        if email == "":
            recipients.remove(email)

    #Send actual email if not in debug mode
    if not settings.DEBUG and len(recipients) > 0:
        mail = django_send_mail(subject, message, fromMail, recipients, fail_silently=fail_silently)
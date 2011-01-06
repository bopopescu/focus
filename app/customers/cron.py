from core.django_cron import cronScheduler, Job
from django.core.mail import send_mail

# This is a function I wrote to check a feedback email address and add it to our database. Replace with your own imports
from django.template.loader import render_to_string

class CheckMail(Job):
        run_every = 400

        k = render_to_string('mail/dailyNotifications.html')
        def job(self):
                # This will be executed every 5 minutes
                send_mail('Oppdateringer', k, ['fredrik@fncit.no'], fail_silently=False)

cronScheduler.register(CheckMail)
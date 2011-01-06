from core.django_cron import cronScheduler, Job
from django.core.mail import send_mail

# This is a function I wrote to check a feedback email address and add it to our database. Replace with your own imports


class CheckMail(Job):
        run_every = 3600

        def job(self):
                # This will be executed every 5 minutes
                send_mail('Dette er en ny melding, som skal komme hver time', 'Here is.', 'fredrik@fncit.no', ['fredrik@fncit.no'], fail_silently=False)

cronScheduler.register(CheckMail)
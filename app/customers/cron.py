from core.django_cron import cronScheduler, Job
from django.core.mail import send_mail

# This is a function I wrote to check a feedback email address and add it to our database. Replace with your own imports


class CheckMail(Job):
        """
                Cron Job that checks the lgr users mailbox and adds any approved senders' attachments to the db
        """

        # run every 300 seconds (5 minutes)
        run_every = 50

        def job(self):
                # This will be executed every 5 minutes
                send_mail('Subject here', 'Here is.', 'fredrik@fncit.no', ['fredrik@fncit.no'], fail_silently=False)

cronScheduler.register(CheckMail)
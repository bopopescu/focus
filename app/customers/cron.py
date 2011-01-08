from core import Core
from core.django_cron import cronScheduler, Job
from django.core.mail import send_mail

# This is a function I wrote to check a feedback email address and add it to our database. Replace with your own imports
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class CheckMail(Job):
        run_every = 400

        def job(self):
            k = render_to_string('mail/dailyNotifications.html', {'companyName': 'Firma',
                                                                'notifications': Core.current_user().get_new_notifications()
                                                                })


            subject, from_email, to = 'hello', 'frecarlsen@gmail.com', 'fredrik@fncit.no'
            text_content = 'This is an important message.'
            html_content = k
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

cronScheduler.register(CheckMail)
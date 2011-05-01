# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import poplib
from email import parser
from app.tickets.models import Ticket, TicketStatus, TicketPriority
from app.tickets.tickets_client_site.models import TicketClient
from core.auth.company.models import Company
from core.auth.user.models import User

class Command(BaseCommand):
    def get_new_emails(self):
        #!/usr/bin/env python
        import poplib
        import email
        import string

        for company in Company.objects.all():

            if company.email_host and company.email_password and company.email_username:

                M = poplib.POP3(company.email_host)
                M.user(company.email_username)
                M.pass_(company.email_password)

                numMessages = len(M.list()[1])
                for i in range(numMessages):
                    print "=" * 40
                    msg = M.retr(i + 1)
                    str = string.join(msg[1], "\n")
                    mail = email.message_from_string(str)

                    email = mail["From"]
                    subject = mail["Subject"]
                    date = mail["Date"]

                    if mail.is_multipart():
                        content = mail.get_payload(0).get_payload()
                    else:
                        content = mail.get_payload()

                    ticketClient, created = TicketClient.objects.get_or_create(email=email)

                    if not ticketClient.id:
                        ticketClient.set_password(ticketClient.generate_password())

                    ticket = Ticket()
                    ticket.title = subject.decode("latin1")
                    ticket.description = content.decode("latin1")
                    ticket.priority = TicketPriority.objects.all()[0]
                    ticket.status = TicketStatus.objects.all()[0]
                    ticket.company = company
                    ticket.save()

                    User.objects.get(username="petter").grant_role("Admin", ticket)

                    ticketClient.tickets.add(ticket)
                    ticketClient.save()

                #if numMessages>0:
                #    M.dele(numMessages)

                M.quit()

        print Ticket.objects.all()

    def handle(self, *apps, **options):
        self.get_new_emails()
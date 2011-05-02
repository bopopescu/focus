# -*- coding: utf-8 -*-
from email.header import decode_header
from email.mime.text import MIMEText
from django.core.management.base import BaseCommand
import poplib
from email import parser
from app.tickets.models import Ticket, TicketStatus, TicketPriority
from app.tickets.tickets_client_site.models import TicketClient
from core import Core
from core.auth.company.models import Company
import re

class Command(BaseCommand):
    def get_new_emails(self):
        import poplib
        import string
        import email

        for company in Company.objects.all():


            if company.admin_group and company.email_host and company.email_password and company.email_username:

                print company.email_host
                
                Core.set_test_user(company.admin_group.members.all()[0])

                M = poplib.POP3(company.email_host)
                M.user(company.email_username)
                M.pass_(company.email_password)


                numMessages = len(M.list()[1])

                for i in range(numMessages):
                    print "=" * 40
                    msg = M.retr(i + 1)
                    str = string.join(msg[1], "\n")
                    str = re.sub(r'\r(?!=\n)', '\r\n', str)

                    str.replace("=E5","å")

                    mail = email.message_from_string((str))

                    email_address = mail["From"]
                    subject = mail["Subject"]

                    k = 3
                    for index in [m.start() for m in re.finditer('\_'+'\?=',subject)]:
                        subject = subject[:index+k] + " " + subject[index+k:]
                        k+=1

                    decoded = decode_header(subject)

                    s = ""

                    for text, encoding in decoded:
                        if encoding:
                            s+= text.decode(encoding)
                        else:
                            s+= text

                    subject = (s)

                    if mail.is_multipart():
                        content = mail.get_payload(0).get_payload()
                    else:
                        content = mail.get_payload()



                    ticketClient, created = TicketClient.objects.get_or_create(email=email_address)

                    if not ticketClient.id:
                        ticketClient.set_password(ticketClient.generate_password())

                    ticket = Ticket()
                    ticket.title = subject

                    encoding = "utf-8"
                    if 'text/plain' in mail["Content-Type"]:
                        encoding = "latin1"

                    ticket.description = content.decode(encoding).strip()

                    ticket.description = ticket.description.replace("=F8",u"ø")
                    ticket.description = ticket.description.replace("=D8",u"Ø")
                    ticket.description = ticket.description.replace("=E6",u"æ")
                    ticket.description = ticket.description.replace("=C6",u"Æ")
                    ticket.description = ticket.description.replace("=E5",u"å")
                    ticket.description = ticket.description.replace("=C5",u"Å")
                    ticket.description = ticket.description.replace("=20",u"\n")

                    print ticket.description

                    ticket.priority = TicketPriority.objects.all()[0]
                    ticket.status = TicketStatus.objects.all()[0]

                    ticket.company = company
                    ticket.save()

                    ticketClient.tickets.add(ticket)
                    ticketClient.save()

                    #if numMessages>0:
                    #    M.dele(numMessages)

                M.quit()

    def handle(self, *apps, **options):
        self.get_new_emails()
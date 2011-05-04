# -*- coding: utf-8 -*-
from email.header import decode_header
from django.core.management.base import BaseCommand
from app.tickets.models import Ticket, TicketStatus, TicketPriority, TicketType
from app.client.models import ClientUser
from core import Core
from core.auth.company.models import Company
import re
from core.mail import send_mail

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

                    mail = email.message_from_string((str))

                    email_address = ""

                    for text, encoding in decode_header(mail["From"]):
                        if encoding:
                            email_address += text.decode(encoding)
                        else:
                            email_address += text

                    address_start = email_address.find("<")+1
                    address_end = email_address.find(">")
                    email_address = email_address[address_start:address_end]

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


                    ticketClient, created = ClientUser.objects.get_or_create(email=email_address)
                    if created:
                        password = ticketClient.generate_password()
                        ticketClient.set_password(password)

                        message = """Hei. Takk for din henvendelse. \n Vi har opprettet en sak hos oss.
                        Du kan følge progresjon og komme med kommenterer ved å logge inn på %s

                        Bruk din epostadresse og passordet: %s

                                    """ % ("http://focus.fncit.no/tickets/client", password)
                    else:
                        message = """Hei. Takk for din henvendelse. \n Vi har opprettet en sak hos oss.
                        Du kan følge progresjon og komme med kommenterer ved å logge inn på %s

                                    """ % ("http://focus.fncit.no/tickets/client")

                    send_mail("Din henvendelse er registrert", message, "no-reply@focussecurity.no", [email_address])

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

                    ticket.priority = TicketPriority.objects.all()[0]
                    ticket.status = TicketStatus.objects.all()[0]
                    ticket.type = TicketType.objects.all()[0]

                    ticket.client_user = ticketClient
                    print company
                    ticket.company = company
                    ticket.save()
                    print "blah"

                    ticketClient.tickets.add(ticket)
                    ticketClient.save()

                if numMessages>0:
                    M.dele(numMessages)

                M.quit()

    def handle(self, *apps, **options):
        self.get_new_emails()
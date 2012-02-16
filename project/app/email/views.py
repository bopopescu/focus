from django.shortcuts import render
from django.http import HttpResponse
from app.email.models import Email
from app.tickets.models import Ticket, TicketUpdate
from libs.postmark.postmark.inbound import PostmarkInbound

def parse(request):

    inbound = PostmarkInbound(json=request.raw_post_data)


    email = Email()

    # content
    email.from_name = inbound.from_name()
    email.from_email = inbound.from_email()
    email.to = inbound.to()

    try:
        email.bcc =  inbound.bcc()
    except:
        pass

    try:
        email.tag = inbound.tag()
    except:
        pass

    try:
        email.message_id = inbound.message_id()
    except:
        pass

    try:
        email.mailbox_hash = inbound.mailbox_hash()
    except:
        pass

    try:
        email.reply_to = inbound.reply_to()
    except:
        pass

    email.html_body = inbound.html_body()
    email.text_body = inbound.text_body()

    email.subject = inbound.subject()


    try:
        email.save()

        print email.mailbox_hash

        if email.mailbox_hash:
            if Ticket.objects.filter(mailbox_hash=email.mailbox_hash).count() > 0:

                ticket = Ticket.objects.get(mailbox_hash=email.mailbox_hash)

                ticket_update = TicketUpdate(ticket=ticket,
                                             company=ticket.company,
                                             comment=email.text_body,
                                             )

                ticket_update.save()



    except Exception, e:
        print str(e)

    return HttpResponse("OK")
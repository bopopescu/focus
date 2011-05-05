from django.http import Http404
from django.shortcuts import render, redirect
from app.client.forms import ClientTicketForm
from app.client.models import ClientUser
from app.client.utils import client_login_required
from app.tickets.forms import EditTicketForm
from app.tickets.models import TicketUpdate, Ticket
from django.utils.translation import ugettext as _
import copy

@client_login_required
def overview(request):
    client = ClientUser.objects.get(id=request.session['client_id'])
    tickets = client.tickets.all()
    return render(request, 'client/tickets/overview.html', {'client': client,
                                                    'tickets': tickets})


@client_login_required
def view(request, id):
    client = ClientUser.objects.get(id=request.session['client_id'])

    try:
        ticket = client.tickets.get(id=id)
        updates = TicketUpdate.objects.filter(ticket=ticket).order_by("id")

    except ClientUser.DoesNotExist:
        raise Http404

    if request.method == "POST":
        ticket_form = ClientTicketForm(request.POST, request.FILES, instance=ticket)

        if ticket_form.is_valid():
            ticket, ticket_update = ticket_form.save()
            ticket_update.client_user = client
            ticket_update.save()
            request.message_success(_("Ticket updated"))

            return redirect(view, ticket.id)
        
    else:
        ticket_form = ClientTicketForm(instance=ticket)

    return render(request, 'client/tickets/ticket_detail.html', {'client': client,
                                                         'ticket': ticket,
                                                         'updates': updates,
                                                         'form': ticket_form,
                                                         })
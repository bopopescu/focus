from django.shortcuts import render, redirect
from app.client.forms import ClientTicketForm, ClientNewTicketForm
from app.client.models import ClientUser
from app.client.utils import client_login_required
from app.tickets.models import TicketUpdate, Ticket
from django.utils.translation import ugettext as _

@client_login_required
def overview(request):
    client = ClientUser.objects.get(id=request.session['client_id'])
    tickets = client.tickets.all()
    return render(request, 'client/tickets/overview.html', {'client': client,
                                                    'tickets': tickets})


@client_login_required
def view(request, id):
    client = ClientUser.objects.get(id=request.session['client_id'])

    ticket = client.tickets.get(id=id)
    updates = TicketUpdate.objects.filter(ticket=ticket).filter(public=True).order_by("id")


    if request.method == "POST":
        ticket_form = ClientTicketForm(request.POST, request.FILES, instance=ticket)

        if ticket_form.is_valid():
            ticket_update = ticket_form.save()
            ticket_update.client_user = client
            ticket_update.public = True
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

@client_login_required
def new_ticket(request):
    client = ClientUser.objects.get(id=request.session['client_id'])
    if request.method == 'POST':
        form = ClientNewTicketForm(client, request.POST)
        if form.is_valid():
            ticket = form.save()


    else:
        form = ClientNewTicketForm(client)

    print form.as_p()

    return render(request, "client/tickets/create_ticket.html", {'form': form})



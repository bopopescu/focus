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
    offers = client.offers.all()
    return render(request, 'client/offers/overview.html', {'client': client,
                                                    'offers': offers})

@client_login_required
def view(request, id):
    client = ClientUser.objects.get(id=request.session['client_id'])

    try:
        offer = client.offers.get(id=id)
    except ClientUser.DoesNotExist:
        raise Http404

    return render(request, 'client/offers/view.html', {'client': client,
                                                         'offer': offer,
                                                         })
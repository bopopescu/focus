from app.tickets.tickets_client_site.models import TicketClient
from hashlib import sha1
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from app.tickets.tickets_client_site.utils import client_login_required


def login(request):
    error = False
    if request.method == 'POST':
        try:
            client = TicketClient.objects.get(email=request.POST['email'])
            if client.check_password(request.POST['password']):
                request.session['client_id'] = client.id
                return HttpResponseRedirect(reverse('client_ticket_overview'))
        except TicketClient.DoesNotExist:
            error = True

    return render(request, "tickets_client_site/login.html", {'error' : error})


@client_login_required
def overview(request):
    client = TicketClient.objects.get(id=request.session['client_id'])
    tickets = client.tickets
    return HttpResponse("test")
    return render(request, 'tickets_client_site/overview.html', {'client': client,
                                                                 'tickets': tickets})


@client_login_required
def view(request, id):
    client = TicketClient.objects.get(id=request.session['client_id'])
    ticket = get_objectg






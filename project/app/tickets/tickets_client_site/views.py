from app.tickets.tickets_client_site.models import TicketClient
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from app.tickets.tickets_client_site.utils import client_login_required


def login(request):
    error = False
    if request.method == 'POST':
        try:
            client = TicketClient.objects.get(email=request.POST['email'])
        except TicketClient.DoesNotExist:
            client = None

        if client and client.check_password(request.POST['password']):
            request.session['client_id'] = client.id
            return redirect(reverse('client_overview'))

        error = True
        
    return render(request, "tickets_client_site/login.html", {'error' : error})

def logout(request):
    try:
        del request.session['client_id']
    except KeyError:
        pass
    return redirect(reverse("client_login"))


@client_login_required
def overview(request):
    client = TicketClient.objects.get(id=request.session['client_id'])
    tickets = client.tickets
    return render(request, 'tickets_client_site/overview.html', {'client': client,
                                                                 'tickets': tickets})


@client_login_required
def view(request, id):
    client = TicketClient.objects.get(id=request.session['client_id'])
    try:
        ticket = client.tickets.get(id=id)
    except TicketClient.DoesNotExist:
        raise Http404
    return render(request, 'tickets_client_site/view.html', {'client': client,
                                                             'ticket': ticket})








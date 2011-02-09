from app.tickets.models import Ticket
from core import Core
from core.shortcuts import render_with_request

def overview(request):
    tickets = Core.current_user().getPermittedObjects("VIEW", Ticket)
    return render_with_request(request, 'tickets/list.html', {"title": "Tickets", "tickets": tickets})


def add(request):
    return overview(request)

from app.tickets.models import Ticket
from core import Core
from core.shortcuts import render_with_request
from core.decorators import login_required
from app.tickets.forms import TicketForm
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _

@login_required()
def overview(request):
    tickets = Core.current_user().getPermittedObjects("VIEW", Ticket)
    return render_with_request(request, 'tickets/list.html', {"title": "Tickets", "tickets": tickets})

def view(request, id):
    pass

@login_required()
def add(request):
    return form(request)

@login_required()
def edit(request, id):
    return form(request, id)


def form(request, id=False):
    if id:
        instance = get_object_or_404(Ticket, id)
        msg = _("Contact changed")
    else:
        instance = Ticket()
        msg = _("Contact added")

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=instance)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.owner = request.user
            ticket.save()
            request.message_success(msg)

            return redirect(edit, ticket.id)
    else:
        form = TicketForm(instance=instance)

    tickets = Core.current_user().getPermittedObjects("VIEW", Ticket)
    print tickets
    return render_with_request(request, "tickets/form.html", {'title': _('Ticket'),
                                                              'form': form,
                                                              'tickets': tickets,
                                                              })





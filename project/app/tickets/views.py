from app.tickets.models import Ticket, TicketUpdate
from core import Core
from core.decorators import require_permission
from core.shortcuts import render_with_request
from app.tickets.forms import TicketForm, EditTicketForm
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
import copy


def overview(request):
    tickets = Core.current_user().get_permitted_objects("VIEW", Ticket).filter(trashed=False)
    return render_with_request(request, 'tickets/list.html', {"title": "Tickets", "tickets": tickets})

def overview_trashed(request):
    tickets = Core.current_user().get_permitted_objects("VIEW", Ticket).filter(trashed=True)
    return render_with_request(request, 'tickets/list.html', {"title": "Tickets", "tickets": tickets})


def view(request, id):
    ticket = Core.current_user().get_permitted_objects("VIEW", Ticket).get(id=id)
    updates = TicketUpdate.objects.filter(ticket=ticket).order_by("-id")

    return render_with_request(request, "tickets/view.html", {'title': _('Ticket'),                                                              
                                                              'ticket': ticket,
                                                              'updates': updates
                                                              })

@require_permission("DELETE", Ticket, "id")
def trash(request, id):
    customer = Ticket.objects.get(id=id)

    if request.method == "POST":
        if not customer.can_be_deleted()[0]:
            request.message_error("You can't delete this customer because: ")
            for reason in customer.can_be_deleted()[1]:
                request.message_error(reason)
        else:
            request.message_success("Successfully deleted this customer")
            customer.trash()
        return redirect(overview)
    else:
        return render_with_request(request, 'tickets/trash.html', {'title': _("Confirm delete"),
                                                                     'customer': customer,
                                                                     'can_be_deleted': customer.can_be_deleted()[0],
                                                                     'reasons': customer.can_be_deleted()[1],
                                                                     })

def add(request):
    return form(request)

def edit(request, id):
    ticket = Core.current_user().get_permitted_objects("VIEW", Ticket).get(id=id)

    if request.method == "POST":
        old_ticket = copy.copy(ticket)
        ticket_form = EditTicketForm(request.POST, request.FILES, instance=ticket)

        if ticket_form.is_valid():
            ticket, ticket_update = ticket_form.save()
            differences = Ticket.find_differences(ticket, old_ticket)
            ticket_update.create_update_lines(differences)
            request.message_success(_("Ticket updated"))

            return redirect(view, ticket.id)

    else:
        ticket_form = EditTicketForm(instance=ticket)

    return render_with_request(request, "tickets/edit.html", {'title': _('Update Ticket'),
                                                              'ticket': ticket,
                                                              'ticket_form': ticket_form,
                                                              })

def form(request, id=False):

    if id:
        instance = Core.current_user().get_permitted_objects("VIEW", Ticket).get(id=id)
        msg = _("Ticket changed")
    else:
        instance = Ticket()
        msg = _("Ticket added")

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.owner = request.user
            ticket.save()
            request.message_success(msg)

            return redirect(view, ticket.id)
    else:
        form = TicketForm(instance=instance)

    return render_with_request(request, "tickets/form.html", {'title': _('Ticket'),
                                                              'ticket':instance,
                                                              'form': form,
                                                              })
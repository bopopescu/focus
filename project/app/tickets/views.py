import simplejson
from app.tickets.models import Ticket, TicketUpdate, TicketType, TicketStatus
from core import Core
from core.auth.user.models import User
from core.decorators import require_permission
from django.shortcuts import render, get_object_or_404
from app.tickets.forms import TicketForm, EditTicketForm, AddTicketTypeForm
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
import copy
from django.http import HttpResponse


@require_permission("LIST", Ticket)
def overview(request, status_id=None):
    tickets = Core.current_user().get_permitted_objects("VIEW", Ticket).filter(trashed=False)
    if status_id:
        status = TicketStatus.objects.get(id=status_id)
        tickets = tickets.filter(status=status)
    return render(request, 'tickets/list.html', {"title": "Tickets", "tickets": tickets})


@require_permission("LIST", Ticket)
def assigned_to_user(request, id=None, status_id=None):
    user = Core.current_user()
    if id:
        user = User.objects.get(id=id)

    tickets = Core.current_user().get_permitted_objects("VIEW", Ticket).filter(trashed=False, assigned_to=user)
    if status_id:
        status = TicketStatus.objects.get(id=status_id)
        tickets = tickets.filter(status=status)

    return render(request, 'tickets/list.html', {"title": "Tickets", "tickets": tickets})


@require_permission("LIST", Ticket)
def overview_trashed(request):
    tickets = Core.current_user().get_permitted_objects("VIEW", Ticket).filter(trashed=True)
    return render(request, 'tickets/list.html', {"title": "Tickets", "tickets": tickets})


@require_permission("VIEW", Ticket, "id")
def view(request, id):
    ticket = Core.current_user().get_permitted_objects("VIEW", Ticket).get(id=id)
    updates = TicketUpdate.objects.filter(ticket=ticket).order_by("-id")

    return render(request, "tickets/view.html", {'title': _('Ticket'),
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
        return render(request, 'tickets/trash.html', {'title': _("Confirm delete"),
                                                      'customer': customer,
                                                      'can_be_deleted': customer.can_be_deleted()[0],
                                                      'reasons': customer.can_be_deleted()[1],
                                                      })


@require_permission("CREATE", Ticket)
def add(request):
    return form(request)


@require_permission("EDIT", Ticket, "id")
def edit(request, id):
    ticket = Core.current_user().get_permitted_objects("VIEW", Ticket).get(id=id)

    if request.method == "POST":
        old_ticket = copy.copy(ticket)
        ticket_form = EditTicketForm(request.POST, request.FILES, instance=ticket)

        if ticket_form.is_valid():
            ticket, ticket_update = ticket_form.save(commit=False)
            ticket.set_user(Core.current_user())
            ticket.save()
            differences = Ticket.find_differences(ticket, old_ticket)
            ticket_update.create_update_lines(differences)
            request.message_success(_("Ticket updated"))

            return redirect(view, ticket.id)

    else:
        ticket_form = EditTicketForm(instance=ticket)

    return render(request, "tickets/edit.html", {'title': _('Update Ticket'),
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
            ticket.set_user(Core.current_user())
            ticket.save()
            request.message_success(msg)

            return redirect(view, ticket.id)
    else:
        form = TicketForm(instance=instance)

    return render(request, "tickets/form.html", {'title': _('Ticket'),
                                                 'ticket': instance,
                                                 'form': form,
                                                 })




@require_permission("CREATE", Ticket)
def add_ticket_type_ajax(request, id=None):
    if id:
        instance = get_object_or_404(TicketType, id=id)
    else:
        instance = TicketType()
    form = AddTicketTypeForm(request.POST, instance=instance)
    if form.is_valid():
        print "blah"
        ticket_type = form.save()
        return HttpResponse(simplejson.dumps({'name': ticket_type.name,
                                              'id': ticket_type.id,
                                              'valid': True}), mimetype='application/json')
    else:
        print form.errors
        errors = dict([(field, errors[0]) for field, errors in form.errors.items()])
        return HttpResponse(simplejson.dumps({'errors': errors,
                                              'valid': False}), mimetype='application/json')


from app.tickets.models import Ticket, Comment
from core import Core
from core.shortcuts import render_with_request
from app.tickets.forms import TicketForm, EditTicketForm, CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _


def overview(request):
    tickets = Core.current_user().getPermittedObjects("VIEW", Ticket)
    return render_with_request(request, 'tickets/list.html', {"title": "Tickets", "tickets": tickets})

def view(request, id):
    ticket = Core.current_user().getPermittedObjects("VIEW", Ticket).get(id=id)
    if request.method == 'POST':
        ticket_form = EditTicketForm(request.POST, instance=ticket, prefix="ticket")
        comment_form = CommentForm(request.POST, instance=Comment(), prefix="comment")

        if ticket_form.is_valid() and comment_form.is_valid():
            ticket_form.save()
            comment_form.save()
            msg = _("Successful update")
            request.message_success(msg)

            return redirect(view, id)


    else:
        ticket_form = EditTicketForm(instance=ticket, prefix="ticket")
        comment_form = CommentForm(instance=Comment(), prefix="comment")

    return render_with_request(request, "tickets/view.html", {'title': _('Ticket'),
                                                              'ticket_form': ticket_form,
                                                              'comment_form': comment_form,
                                                              })

def add(request):
    return form(request)


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
    return render_with_request(request, "tickets/form.html", {'title': _('Ticket'),
                                                              'form': form,
                                                              'tickets': tickets,
                                                              })





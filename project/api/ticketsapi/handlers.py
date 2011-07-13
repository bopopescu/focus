from piston.handler import BaseHandler
from piston.utils import rc
from app.tickets.models import Ticket, TicketType, TicketStatus
from core import Core
from django.core import urlresolvers
from core.auth.user.models import User

class TicketHandler(BaseHandler):
    model = Ticket
    allowed_methods = ('GET', )
    fields = (
        'id', 'ticket_creator', 'title', 'mark_as_unread_for_current_user', ('user',('id','get_full_name')),'get_recipients', ('priority', ('name',)), 'update_count',
            ('status', ('name',)),
            ('type', ('name',)), 'date_edited', ('assigned_to', ('username', 'get_full_name')), 'ticket_url' )

    @classmethod
    def update_count(cls, ticket):
        return len(ticket.updates.all())

    @classmethod
    def ticket_creator(cls, ticket):
        try:
            return ticket.creator.username
        except AttributeError:
            return ticket.creator.email

    @classmethod
    def ticket_url(cls, ticket):
        return urlresolvers.reverse('app.tickets.views.view', args=(ticket.id, ))

    @classmethod
    def date_edited(cls, ticket):
        return ticket.date_edited.strftime("%d.%m.%Y %H:%S")

    def read(self, request, id=None):
        all = Core.current_user().get_permitted_objects("VIEW", Ticket)
        if id:
            try:
                return all.get(id=id)
            except Ticket.DoesNotExist:
                return rc.NOT_FOUND
        else:
            all = TicketHandler.filter_tickets(all, request.GET)
            return all

    @staticmethod
    def filter_tickets(tickets, filter):
        type_id = int(filter.get('type_id', False))
        if type_id:
            type = TicketType.objects.get(id=type_id)
            tickets = tickets.filter(type=type)

        status_id = int(filter.get('status_id', False))
        if status_id:
            status = TicketStatus.objects.get(id=status_id)
            tickets = tickets.filter(status=status)

        assigned_to = int(filter.get('assigned_to', False))
        if assigned_to:
            assigned_to = User.objects.get(id=assigned_to)
            tickets = tickets.filter(assigned_to=assigned_to)

        trashed = bool(int(filter.get('trashed', False)))
        tickets = tickets.filter(trashed=trashed)

        return tickets
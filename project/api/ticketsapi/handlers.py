from piston.handler import BaseHandler
from piston.utils import rc
from app.tickets.models import Ticket, TicketType
from core import Core
from django.core import urlresolvers

class TicketHandler(BaseHandler):
    model = Ticket
    allowed_methods = ('GET', )
    fields = ('id', 'ticket_creator', 'title', ('priority', ('name',)), 'update_count', ('status', ('name',)),
              ('type', ('name',)), 'date_edited', ('assigned_to', ('username',)), 'ticket_url' )

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

    def read(self, request, id=None):
        all = Core.current_user().get_permitted_objects("VIEW", Ticket)
        if id:
            try:
                return all.get(id=id)
            except Ticket.DoesNotExist:
                return rc.NOT_FOUND
        else:
            type_id = int(request.GET.get('type_id', False))
            if type_id:
                type = TicketType.objects.get(id=type_id)
                all = all.filter(type=type)
            return all

    





    
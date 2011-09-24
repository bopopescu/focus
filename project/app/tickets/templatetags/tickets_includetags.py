from django import template
from app.tickets.models import TicketStatus, TicketType
from core import Core
import settings

register = template.Library()

@register.inclusion_tag("tickets/sidebar.html")
def tickets_sidebar(request):
    return {
        'statuses': TicketStatus.objects.all(),
        'STATIC_URL': settings.STATIC_URL,
        'request': request,
    }

@register.inclusion_tag("tickets/type_filter.html")
def tickets_type_filter(request):
    return {
        'types': TicketType.objects.filter(company=Core.current_user().get_company()),
        'request': request,
    }
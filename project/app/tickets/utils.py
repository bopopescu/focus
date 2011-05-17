from django.utils.translation import ugettext as _
from core.mail import send_mail
import settings


def send_assigned_mail(user, ticket, assigned=True):
    if assigned:
        msg = _("You have been assigned to the ticket %s a") % ticket.title
    else:
        msg = _("You have been unassigned from the the ticket %s u") % ticket.title

    send_mail(ticket.title, msg, settings.NO_REPLY_EMAIL, [user.email])


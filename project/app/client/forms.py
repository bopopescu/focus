from django.forms.models import ModelForm
from app.tickets.models import Ticket, TicketUpdate
from django import forms
from django.utils.translation import ugettext as _

class ClientTicketForm(ModelForm):
    comment = forms.CharField(widget=forms.Textarea, label=_("Add Comment"), required=False)
    attachment = forms.FileField(label=_("Add Attachment"), required=False)

    class Meta:
        model = Ticket
        fields = ()

    def save(self, *args, **kwargs):
        ticket = super(ClientTicketForm, self).save()

        ticketupdate = TicketUpdate.objects.create(ticket=ticket,
                                                   comment=self.cleaned_data['comment'],
                                                   attachment=self.cleaned_data['attachment'])

        return ticket, ticketupdate




from django.forms.models import ModelForm
from app.tickets.models import Ticket, TicketUpdate, TicketType
from django import forms
from django.utils.translation import ugettext as _


class ClientTicketForm(ModelForm):
    """
    Form for making comments
    """
    comment = forms.CharField(widget=forms.Textarea, label=_("Add Comment"))
    attach = forms.FileField(label=_("Add Attachment"), required=False)

    class Meta:
        model = Ticket
        fields = ()


    def save(self, *args, **kwargs):
        ticket = super(ClientTicketForm, self).save()
        ticketupdate = TicketUpdate.objects.create(ticket=ticket,
                                                   comment=self.cleaned_data['comment'],
                                                   attachment=self.cleaned_data['attach'])

        return ticketupdate


class ClientNewTicketForm(ModelForm):
    """ Form for creating new tickets """

    client = None

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'company')


    def __init__(self, client, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.client = client
        self.fields['company'].queryset = client.get_related_companys()
        self.fields['company'].empty_label = None

    def save(self, commit=True):
        ticket = super(ClientNewTicketForm, self).save(commit=False)
        ticket.client_user = self.client
        ticket.type = TicketType.objects.get_or_create(name=_("Client ticket"),
                                                       company=self.cleaned_data['company'],
                                                       description=_("Submitted by a client"))[0]
        ticket.save(commit=commit)
        self.client.tickets.add(ticket)

        return ticket

        

    

    




from app.orders.models import Order
from django.forms.models import ModelForm
from app.customers.models import Customer
from app.tickets.models import Ticket, TicketUpdate, TicketType
from core import Core
from core.models import User
from django import forms
from django.utils.translation import ugettext as _
from core.widgets import SelectWithPop, DatePickerField

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = (
            'title', 'customer', 'description', 'status', 'priority', 'type', 'due_date', 'assigned_to',
            'attachment', "order")

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter_current_company()
        self.fields['attachment'].required = False
        self.fields['customer'].widget = SelectWithPop(Customer)
        self.fields['customer'].queryset = Customer.objects.filter_current_company()
        self.fields['order'].queryset = Order.objects.filter_current_company()
        self.fields['type'].widget = SelectWithPop(TicketType)
        self.fields['type'].queryset = TicketType.objects.filter(company=Core.current_user().get_company())
        self.fields['due_date'].required = False
        self.fields['due_date'].widget = DatePickerField(format="%d.%m.%Y")
        self.fields['due_date'].input_formats = ["%d.%m.%Y"]


class EditTicketForm(ModelForm):
    comment = forms.CharField(widget=forms.Textarea, label=_("Add Comment"), required=False)
    attachment = forms.FileField(label=_("Add Attachment"), required=False)
    public = forms.BooleanField(label=_("Make comment public"), required=False)

    class Meta:
        model = Ticket
        fields = (
            'title', 'customer', 'status', 'priority', 'type', 'due_date', 'assigned_to', 'order',)

    def __init__(self, *args, **kwargs):
        super(EditTicketForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter_current_company()
        self.fields['customer'].widget = SelectWithPop(Customer)
        self.fields['customer'].queryset = Customer.objects.filter_current_company()
        self.fields['order'].queryset = Order.objects.filter_current_company()
        self.fields['type'].widget = SelectWithPop(TicketType)
        self.fields['type'].queryset = TicketType.objects.filter(company=Core.current_user().get_company())
        self.fields['due_date'].widget = DatePickerField(format="%d.%m.%Y", )
        self.fields['due_date'].input_formats = ["%d.%m.%Y"]

    def save(self, *args, **kwargs):
        ticket = super(EditTicketForm, self).save(*args, **kwargs)
        ticket_update = TicketUpdate(ticket=ticket,
                                     company=ticket.company,
                                     comment=self.cleaned_data['comment'],
                                     attachment=self.cleaned_data['attachment'],
                                     public=self.cleaned_data['public'])

        if kwargs.get('commit', False):
            ticket_update.save()

        return ticket, ticket_update


class AddTicketTypeForm(ModelForm):
    class Meta:
        model = TicketType
        fields = ('name', 'description')


class AddClientForm(forms.Form):
    email = forms.EmailField()
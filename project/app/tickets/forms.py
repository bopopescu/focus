from django.forms.models import ModelForm
from app.tickets.models import Ticket, TicketStatus, TicketPriority, TicketType
from django.forms.forms import Form
from django import forms

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'customer', 'description', 'status', 'priority', 'type', 'estimated_time', 'assigned_to', 'comments')


class UpdateTicketForm(Form):
    status = forms.ModelChoiceField(queryset=TicketStatus.objects.all)
    priority = forms.ModelChoiceField(queryset=TicketPriority.objects.all)
    type = forms.ModelChoiceField(queryset=TicketType.objects.all)
    spent_time = forms.IntegerField()


    

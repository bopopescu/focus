from django.forms.models import ModelForm
from app.tickets.models import Ticket
from core.models import User

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'customer', 'description', 'status', 'priority', 'type', 'estimated_time', 'assigned_to',)

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.inCompany()

class EditTicketForm(ModelForm):
    class Meta:
        model = Ticket
        include = ('status', 'priority', 'type', 'spent_time', 'estimated_time', 'assigned_to',)
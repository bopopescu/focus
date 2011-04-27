from django.forms.models import ModelForm
from app.hourregistrations.models import HourRegistration
from app.orders.models import Order
from core import Core
from core.widgets import DatePickerField, MaskedField

class HourRegistrationForm(ModelForm):
    class Meta:
        model = HourRegistration
        fields = ("order", "time_start", "time_end", "pause", "description")

    def __init__(self, *args, **kwargs):
        super(HourRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['time_start'].widget = MaskedField(format="99:99")
        self.fields['time_end'].widget = MaskedField(format="99:99")
        self.fields['time_start'].widget.attrs['class'] = 'time_input'
        self.fields['time_end'].widget.attrs['class'] = 'time_input'
        self.fields['order'].queryset = Core.current_user().get_permitted_objects("VIEW", Order)

        if 'instance' in kwargs:
            self.id = kwargs['instance'].id
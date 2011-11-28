from django.forms.models import ModelForm
from django import forms
from app.hourregistrations.models import HourRegistration, HourRegistrationType, Disbursement
from app.orders.models import Order
from core import Core
from core.widgets import DatePickerField


class HourRegistrationForm(ModelForm):
    class Meta:
        model = HourRegistration
        fields = ("order", "time_start", "time_end", 'hours', 'type', "description")

    def __init__(self, *args, **kwargs):
        super(HourRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['time_start'].widget.attrs['class'] = 'time_input'
        self.fields['time_end'].widget.attrs['class'] = 'time_input'

        self.fields['type'].queryset = HourRegistrationType.objects.filter(trashed=False,
                                                                           company=Core.current_user().get_company())

        self.fields['order'].queryset = Core.current_user().get_permitted_objects("VIEW", Order).filter(trashed=False)

        if 'instance' in kwargs:
            self.id = kwargs['instance'].id


class HourRegistrationTypeForm(ModelForm):
    class Meta:
        model = HourRegistrationType
        fields = ('name', 'rate')


class DisbursementForm(ModelForm):
    class Meta:
        model = Disbursement
        fields = ('date', 'order', 'rate', 'count', 'description', 'attachment')

    def __init__(self, *args, **kwargs):
        super(DisbursementForm, self).__init__(*args, **kwargs)
        self.fields['date'].required = False
        self.fields['date'].input_formats = ["%d.%m.%Y"]
        self.fields['date'].widget = DatePickerField(format="%d.%m.%Y")
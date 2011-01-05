# -*- coding: utf-8 -*-
from datetime import date
from django.forms import ModelForm
from app.hourregistrationsOLD.helpers import generateValidPeriode, validForEdit
from models import *
from core.widgets import *

class HourRegistrationForm(ModelForm):
    #order = forms.ModelChoiceField(Order.objects.all(), widget=SelectWithPop())
    #typeOfWork = forms.ModelChoiceField(TypeOfTimeTracking.objects.all(), widget=SelectWithPop())

    class Meta:
        model = HourRegistration
        exclude = (
        'deleted', 'date_created', 'date_edited', 'owner', 'creator', 'hourly_rate', 'percent_cover', 'editor',
        'company', 'hours_worked')

    def __init__(self, *args, **kwargs):
        super(TimetrackingForm, self).__init__(*args, **kwargs)
        self.fields['date'].required = True
        self.fields['date'].widget = DatePickerField(format="%d.%m.%Y", from_date=generateValidPeriode()[0],
                                                     to_date=generateValidPeriode()[1])
        self.fields['date'].input_formats = ["%d.%m.%Y"]

        self.fields['time_start'].widget = MaskedField(format="99:99")
        self.fields['time_end'].widget = MaskedField(format="99:99")

    def clean_date(self):
        date = self.cleaned_data['date']

        if not validForEdit(date.strftime("%d.%m.%Y")):
            raise forms.ValidationError(u"Du kan ikke velge denne datoen, den er utenfor aktiv periode.")

        return date

    def clean_time_start(self):
        time = self.cleaned_data['time_start']

        if not re.match("^(20|21|22|23|[01]\d|\d)(([:][0-5]\d){1,2})$", time):
            raise forms.ValidationError(u"Ugyldig klokkeformat, feks: 16:00")

        return time

    def clean_time_end(self):
        time = self.cleaned_data['time_end']

        if not re.match("^(20|21|22|23|[01]\d|\d)(([:][0-5]\d){1,2})$", time):
            raise forms.ValidationError(u"Ugyldig klokkeformat, feks: 16:00")

        return time

class TypeOfHourRegistrationForm(ModelForm):
    class Meta:
        model = TypeOfHourRegistration
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company')
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import *

from core.widgets import *

class TimetrackingForm(ModelForm):
    date = forms.DateField(required=True, input_formats=["%d.%m.%Y"], widget=DatePickerField(format="%d.%m.%Y"))
    #order = forms.ModelChoiceField(Order.objects.all(), widget=SelectWithPop())
    #typeOfWork = forms.ModelChoiceField(TypeOfTimeTracking.objects.all(), widget=SelectWithPop())
    
    class Meta:
        model = Timetracking
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company', 'hours_worked')

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

class TypeOfTimeTrackingForm(ModelForm):
    class Meta:
        model = TypeOfTimeTracking
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company')
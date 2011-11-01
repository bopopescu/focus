# -*- coding: utf-8 -*-
from django.forms import forms
from django.forms import ModelForm
from app.calendar.models import Event, RepeatOption, EventType
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from core import Core
from core.auth.user.models import User
from core.widgets import DatePickerField


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'type', 'start', 'end', 'description', 'users')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start'].required = True
        self.fields['start'].input_formats = ["%d.%m.%Y"]
        self.fields['start'].widget = DatePickerField(format="%d.%m.%Y")
        self.fields['end'].required = True
        self.fields['end'].input_formats = ["%d.%m.%Y"]
        self.fields['end'].widget = DatePickerField(format="%d.%m.%Y")

        self.fields['type'].queryset = EventType.objects.filter_current_company()
        self.fields['users'].queryset = User.objects.filter_current_company()


class RepeatOptionForm(ModelForm):
    class Meta:
        model = RepeatOption
        fields = ('available_option', 'times', 'repeat_until')

    def __init__(self, *args, **kwargs):
        super(RepeatOptionForm, self).__init__(*args, **kwargs)
        self.fields['repeat_until'].required = False
        self.fields['repeat_until'].input_formats = ["%d.%m.%Y"]
        self.fields['repeat_until'].widget = DatePickerField(format="%d.%m.%Y")


class EventTypeForm(ModelForm):
    class Meta:
        model = EventType
        fields = ('name','color')
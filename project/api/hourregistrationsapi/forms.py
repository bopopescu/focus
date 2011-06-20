from django.forms.models import ModelForm
from api.hourregistrationsapi.models import TimeTracker

class TimeTrackerForm(ModelForm):
    class Meta:
        model = TimeTracker
        fields = ('name', )
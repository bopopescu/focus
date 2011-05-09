from django.forms.models import ModelForm
from app.customers.models import Customer
from app.orders.models import Offer
from app.projects.models import Project
from core.widgets import SelectWithPop, DatePickerField

class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ("offer_number", "title", "customer", "project", 'delivery_date',
                  'delivery_date_deadline', 'description')

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['customer'].widget = SelectWithPop(Customer)
        self.fields['customer'].queryset = Customer.objects.filter_current_company()
        self.fields['project'].widget = SelectWithPop(Project)
        self.fields['project'].queryset = Project.objects.filter_current_company()
        self.fields['delivery_date'].required = False
        self.fields['delivery_date'].input_formats = ["%d.%m.%Y"]
        self.fields['delivery_date'].widget = DatePickerField(format="%d.%m.%Y")
        self.fields['delivery_date_deadline'].required = False
        self.fields['delivery_date_deadline'].input_formats = ["%d.%m.%Y"]
        self.fields['delivery_date_deadline'].widget = DatePickerField(format="%d.%m.%Y")

from django.forms.models import ModelForm
from django import forms
from app.customers.models import Customer
from app.orders.models import Offer, Order
from app.projects.models import Project
from core.widgets import SelectWithPop, DatePickerField
from django.utils.translation import ugettext as _

class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ("offer_number", "title", "customer", "project", 'delivery_date',
                  'delivery_date_deadline', 'accepted', 'description')

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


class CreateOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ("order_number", )

    def clean_order_number(self):
        order_number = self.cleaned_data['order_number']

        orders = Order.objects.filter_current_company()

        for i in orders:
            if i.order_number == order_number:
                raise forms.ValidationError(_("You need to use a unique order number"))

        return order_number

class AddClientForm(forms.Form):
    email = forms.EmailField()
from django.forms.models import ModelForm
from django import forms
from app.customers.models import Customer
from app.orders.models import Offer, Order, Invoice
from app.projects.models import Project
from core.auth.permission.models import Role
from core.auth.user.models import User
from core.widgets import SelectWithPop, DatePickerField
from django.utils.translation import ugettext as _

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ("order_number", "title", "status", "customer", "project", 'delivery_date',
                  'delivery_date_deadline', 'description')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
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

        if 'instance' in kwargs:
            self.id = kwargs['instance'].id

    def clean_order_number(self):
        order_number = self.cleaned_data['order_number']

        orders = Order.objects.filter_current_company()

        for i in orders:
            if self.id == i.id:
                continue
            if i.order_number == order_number:
                raise forms.ValidationError(_("You need to use a unique order number"))

        return order_number


class CreateInvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ("invoice_number", )

    def clean_invoice_number(self):
        invoice_number = self.cleaned_data['invoice_number']

        invoices = Invoice.objects.filter_current_company()

        for i in invoices:
            if i.invoice_number == invoice_number:
                raise forms.ValidationError(_("You need to use a unique invoice number"))

        return invoice_number

class AddParticipantToOrderForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.none)
    role = forms.ModelChoiceField(queryset=Role.objects.none)

    def __init__(self, *args, **kwargs):
        super(AddParticipantToOrderForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset= User.objects.filter_current_company()
        self.fields['role'].queryset = Role.objects.all()

    
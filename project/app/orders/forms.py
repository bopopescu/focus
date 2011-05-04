# -*- coding: utf-8 -*-
from django.forms import ModelForm
from app.customers.models import Customer
from app.orders.models import Order, OrderLine
from app.projects.models import Project
from app.stock.forms import ProductField
from core.auth.user.models import User
from core.widgets import *
from core.shortcuts import get_company_users
from django.utils.translation import ugettext as _


class OrderForm(ModelForm):
    #delivery_date = forms.DateField(required=True, input_formats=["%d.%m.%Y"],
    #                                widget=DatePickerField(format="%d.%m.%Y"))
    #delivery_date_deadline = forms.DateField(required=True, input_formats=["%d.%m.%Y"],
    #                                         widget=DatePickerField(format="%d.%m.%Y"))

    class Meta:
        model = Order
        fields = ("order_number", "PO_number", "title", "customer", "project", "responsible", 'delivery_date',
                  'delivery_date_deadline', 'description')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['customer'].widget = SelectWithPop(Customer)
        self.fields['customer'].queryset = Customer.objects.filter_current_company()
        self.fields['project'].widget = SelectWithPop(Project)
        self.fields['project'].queryset = Project.objects.filter_current_company()
        self.fields['responsible'].queryset = User.objects.filter_current_company()
        self.fields['delivery_date'].required = False
        self.fields['delivery_date'].input_formats = ["%d.%m.%Y"]
        self.fields['delivery_date'].widget = DatePickerField(format="%d.%m.%Y")
        self.fields['delivery_date_deadline'].required = False
        self.fields['delivery_date_deadline'].input_formats = ["%d.%m.%Y"]
        self.fields['delivery_date_deadline'].widget = DatePickerField(format="%d.%m.%Y")

        if 'instance' in kwargs:
            self.id = kwargs['instance'].id

    def clean_delivery_date_deadline(self):
        delivery_date = self.cleaned_data['delivery_date']
        delivery_date_deadline = self.cleaned_data['delivery_date_deadline']

        if delivery_date_deadline < delivery_date:
            raise forms.ValidationError(u"Tidsfristen må være etter leveringsdato")

        return delivery_date

    def clean_order_number(self):
        order_number = self.cleaned_data['order_number']

        orders = Order.objects.filter_current_company()
        for i in orders:
            if self.id == i.id:
                continue

            if i.order_number == order_number:
                raise forms.ValidationError("Det kreves unikt ordrenr")

        return order_number


class OfferForm(OrderForm):
    class Meta:
        model = Order
        fields = ("title", "customer", "project", "responsible", 'delivery_date',
                  'delivery_date_deadline', 'description')


class OrderLineForm(ModelForm):
    product = ProductField()

    class Meta:
        model = OrderLine
        fields = ("product", "count",)


class OrderFormSimple(ModelForm):
    class Meta:
        model = Order
        exclude = (
        'deleted', 'trashed', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company', 'contacts',
        'participant', 'description')
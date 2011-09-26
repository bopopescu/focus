# -*- coding: utf-8 -*-
from app.contacts.models import Contact
from app.orders.models import Order, Offer, Invoice
from app.projects.models import Project
from app.stock.models import Product, Currency
from app.suppliers.models import Supplier
from app.tickets.models import Ticket, TicketStatus, TicketPriority, TicketType
from core import Core
from django.core.management.base import BaseCommand
from app.admin.views.user import generate_new_password_for_user
from app.customers.models import Customer
from app.migratefocus.management.commands.migratefocus import createNewCustomer
import random

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        randomCompanyIdentifier = str(int(random.random() * 99999))

        company, user = createNewCustomer("Ledere", "Bjarte Hatlenes", "superadmin" + randomCompanyIdentifier,
                                          "superadmin" + randomCompanyIdentifier, "Ansatte",
                                          "Focus Security AS" + randomCompanyIdentifier)

        self.company = company
        self.user = user

        Core.set_test_user(user)
        password = generate_new_password_for_user(user)
        print "Company: %s " % company
        print "Current user is: %s " % Core.current_user()
        print "Current user is: %s " % Core.current_user().username
        print "Current users password: %s " % password

        self.seed_customers()
        self.seed_contacts()
        self.seed_orders()
        self.seed_projects()
        self.seed_offers()
        self.seed_tickets()
        self.seed_suppliers()
        self.seed_products()

    def seed_customers(self):
        print "customers"
        for i in range(1, 12):
            Customer.objects.get_or_create(name="Customer %s" % i, company=self.company, cid=i)

    def seed_tickets(self):
        status, created = TicketStatus.objects.get_or_create(name="standard", order_priority=1)
        priority, created = TicketPriority.objects.get_or_create(name="standard")
        type, created = TicketType.objects.get_or_create(name="Type", company=self.company)

        print "tickets"
        for i in range(1, 12):
            ticket, created = Ticket.objects.get_or_create(title="Ticket %s" % i, description="dummy text", type=type, company=self.company,
                                                           priority=priority, status=status)
            ticket.set_user(Core.current_user())
            ticket.save()

    def seed_projects(self):
        print "projects"
        for i in range(1, 12):
            Project.objects.get_or_create(project_name="Project %s" % i, company=self.company, pid=i)

    def seed_orders(self):
        print "orders"
        for i in range(1, 12):
            order, created = Order.objects.get_or_create(title="Order %s" % i, order_number=i, company=self.company)

            if i % 3 == 0:
                Invoice.objects.get_or_create(title="Invoice %s" % i,
                                              invoice_number=Invoice.calculate_next_invoice_number(),
                                              company=self.company,
                                              order=order)

    def seed_offers(self):
        print "offers"
        for i in range(1, 12):
            Offer.objects.get_or_create(title="Offer %s" % i, offer_number=i, company=self.company)

    def seed_contacts(self):
        print "contacts"
        for i in range(1, 12):
            Contact.objects.get_or_create(name="Contact %s" % i, company=self.company)

    def seed_suppliers(self):
        print "suppliers"
        for i in range(1, 12):
            Supplier.objects.get_or_create(name="Supplier %s" % i, company=self.company)

    def seed_products(self):
        print "suppliers"
        price_val, created = Currency.objects.get_or_create(name="Norsk krone")

        for i in range(1, 12):
            Product.objects.get_or_create(name="Supplier %s" % i, company=self.company, priceVal=price_val)
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
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
import random
from core.auth.company.models import Company
from core.auth.group.models import Group
from core.auth.log.models import Notification, Log
from core.auth.user.models import User
from core.utils import get_class

def createNewCustomer(admin_group, adminuser_name, adminuser_password, adminuser_username, all_employees_group, name):
    admin_group = Group(name=admin_group)
    admin_group.save_without_permissions()
    all_employees_group = Group(name=all_employees_group)
    all_employees_group.save_without_permissions()
    company = Company(name=name, admin_group=admin_group, all_employees_group=all_employees_group)
    company.save()

    #Create the admin user
    user = User(first_name=adminuser_name, username=adminuser_username)
    user.set_password(adminuser_password)
    user.company = company
    user.save()

    #Manually give permission to the admin group
    admin_group.grant_permissions("ALL", admin_group)
    admin_group.grant_permissions("ALL", all_employees_group)

    #Add admin user to admin group
    admin_group.add_member(user)

    #Set the company fields on groups
    admin_group.company = company
    admin_group.save()
    all_employees_group.company = company
    all_employees_group.save()

    #Give admin group all permissions on classes
    admin_group.grant_role("Admin", Project)
    admin_group.grant_role("Admin", Customer)
    admin_group.grant_role("Admin", Contact)
    admin_group.grant_role("Admin", Offer)
    admin_group.grant_role("Admin", Invoice)
    admin_group.grant_role("Admin", Order)
    admin_group.grant_role("Admin", get_class("hourregistrations", "hourregistration"))
    admin_group.grant_role("Admin", get_class("hourregistrations", "hourregistrationtype"))
    admin_group.grant_role("Admin", get_class("announcements", "announcement"))
    admin_group.grant_role("Admin", Product)
    admin_group.grant_role("Admin", Log)
    admin_group.grant_role("Admin", Supplier)
    admin_group.grant_role("Admin", Notification)
    admin_group.grant_role("Admin", User)
    admin_group.grant_role("Admin", Group)
    admin_group.grant_role("Admin", Ticket)
    admin_group.grant_permissions("CONFIGURE", Company)

    #Give employee group some permissions on classes
    all_employees_group.grant_role("Member", Project)
    all_employees_group.grant_role("Member", Customer)
    all_employees_group.grant_role("Member", Contact)
    all_employees_group.grant_role("Member", Order)
    all_employees_group.grant_role("Member", Invoice)
    all_employees_group.grant_role("Member", Offer)
    all_employees_group.grant_role("Member", get_class("hourregistrations", "hourregistration"))
    all_employees_group.grant_role("Member", get_class("announcements", "announcement"))
    all_employees_group.grant_role("Member", Product)
    all_employees_group.grant_role("Member", Log)
    all_employees_group.grant_role("Member", Supplier)
    all_employees_group.grant_role("Member", Ticket)
    all_employees_group.grant_role("Member", Notification)

    return company, user


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

        self.customers = []
        self.projects = []

        self.seed_customers()
        self.seed_contacts()
        self.seed_projects()
        self.seed_orders()
        self.seed_offers()
        self.seed_tickets()
        self.seed_suppliers()
        self.seed_products()

    def seed_customers(self):
        print "customers"
        for i in range(1, 10):
            c = Customer.objects.get_or_create(email="email%s@company.com" % i, address="Address %s" % i,
                                               phone="%s%s%s%s%s%s%s%s" % (i, i, i, i, i, i, i, i),
                                               name="Customer %s" % i, company=self.company, cid=i)
            self.customers.append(c[0])

    def seed_tickets(self):
        status, created = TicketStatus.objects.get_or_create(name="standard", order_priority=1)
        priority, created = TicketPriority.objects.get_or_create(name="standard")
        type, created = TicketType.objects.get_or_create(name="Type", company=self.company)

        print "tickets"
        for i in range(1, 10):
            ticket, created = Ticket.objects.get_or_create(title="Ticket %s" % i, description="dummy text", type=type,
                                                           company=self.company,
                                                           priority=priority, status=status)
            ticket.set_user(Core.current_user())
            ticket.save()

    def seed_projects(self):
        print "projects"
        for i in range(1, 10):
            c = Project.objects.get_or_create(project_name="Project %s" % i,
                                              deliveryDate=datetime.now() + timedelta(days=i),
                                              customer=self.customers[int(random.random() * 9)], company=self.company,
                                              pid=i)

            self.projects.append(c[0])

    def seed_orders(self):
        print "orders"
        for i in range(1, 12):
            order, created = Order.objects.get_or_create(title="Order %s" % i,
                                                         delivery_date=datetime.now() + timedelta(days=i),
                                                         customer=self.customers[int(random.random() * 9)],
                                                         project=self.projects[int(random.random() * 9)],
                                                         status="%s" % int(random.random() * 3),
                                                         company=self.company)

            if not i % 3:
                Invoice.objects.get_or_create(title="Invoice %s" % i,
                                              invoice_number=Invoice.calculate_next_invoice_number(),
                                              company=self.company,
                                              delivery_date=datetime.now() + timedelta(days=i),
                                              customer=self.customers[int(random.random() * 9)],
                                              project=self.projects[int(random.random() * 9)],
                                              status="%s" % int(random.random() * 3),
                                              order=order)

    def seed_offers(self):
        print "offers"
        for i in range(1, 12):
            Offer.objects.get_or_create(title="Offer %s" % i, offer_number=i,
                                        delivery_date=datetime.now() + timedelta(days=i),
                                        accepted="%s" % int(random.random() * 3),
                                        customer=self.customers[int(random.random() * 9)],
                                        project=self.projects[int(random.random() * 9)],
                                        company=self.company)

    def seed_contacts(self):
        print "contacts"
        for i in range(1, 12):
            Contact.objects.get_or_create(name="Contact %s" % i, email="email%s@company.com" % i,
                                          address="Address %s" % i, phone="%s%s%s%s%s%s%s%s" % (i, i, i, i, i, i, i, i),
                                          company=self.company)

    def seed_suppliers(self):
        print "suppliers"
        for i in range(1, 12):
            Supplier.objects.get_or_create(name="Supplier %s" % i, company=self.company)

    def seed_products(self):
        print "products"
        price_val, created = Currency.objects.get_or_create(name="Norsk krone")

        for i in range(1, 12):
            Product.objects.get_or_create(name="Product %s" % i, company=self.company, priceVal=price_val)
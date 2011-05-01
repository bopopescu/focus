# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType

from django.core.management.base import BaseCommand
import os
import MySQLdb
import MySQLdb.cursors
from app.hourregistrations.models import HourRegistration
from core import Core
#from core.models import User, Group, Company, Log, Notification
from core.auth.user.models import User
from core.auth.group.models import Group
from core.auth.company.models import Company
from core.auth.log.models import Log, Notification

import random
from app.admin.views.user import generate_new_password_for_user
from core.utils import get_class


Customer = get_class("customers", "customer")
Project = get_class("projects", "project")
Order = get_class("orders", "order")
Supplier = get_class("suppliers", "supplier")
Contact = get_class("contacts", "contact")
Product = get_class("stock", "product")
UnitsForSizes = get_class("stock", "unitsforsizes")
Currency = get_class("stock", "currency")
ProductCategory = get_class("stock", "productcategory")
ProductGroup = get_class("stock", "productgroup")
Ticket = get_class("tickets", "ticket")

def createNewCustomer(adminGroup, adminuserName, adminuserPassword, adminuserUsername, allEmployeesGroup, name):
    adminGroup = Group(name=adminGroup)
    adminGroup.save_without_permissions()
    allEmployeesGroup = Group(name=allEmployeesGroup)
    allEmployeesGroup.save_without_permissions()
    company = Company(name=name, adminGroup=adminGroup, allEmployeesGroup=allEmployeesGroup)
    company.save()

    #Create the admin user
    user = User(first_name=adminuserName, username=adminuserUsername)
    user.set_password(adminuserPassword)
    user.company = company
    user.save()

    #Manually give permission to the admin group
    adminGroup.grant_permissions("ALL", adminGroup)
    adminGroup.grant_permissions("ALL", allEmployeesGroup)

    #Add admin user to admin group
    adminGroup.add_member(user)

    #Set the company fields on groups
    adminGroup.company = company
    adminGroup.save()
    allEmployeesGroup.company = company
    allEmployeesGroup.save()

    #Give admin group all permissions on classes
    adminGroup.grant_role("Admin", Project)
    adminGroup.grant_role("Admin", Customer)
    adminGroup.grant_role("Admin", Contact)
    adminGroup.grant_role("Admin", Order)
    adminGroup.grant_role("Admin", get_class("hourregistrations", "hourregistration"))
    adminGroup.grant_role("Admin", get_class("announcements", "announcement"))
    adminGroup.grant_role("Admin", Product)
    adminGroup.grant_role("Admin", Log)
    adminGroup.grant_role("Admin", Supplier)
    adminGroup.grant_role("Admin", Notification)
    adminGroup.grant_role("Admin", User)
    adminGroup.grant_role("Admin", Group)
    adminGroup.grant_role("Admin", Ticket)
    adminGroup.grant_permissions("CONFIGURE", Company)

    #Give employee group some permissions on classes
    allEmployeesGroup.grant_role("Admin", Project)
    allEmployeesGroup.grant_role("Admin", Customer)
    allEmployeesGroup.grant_role("Admin", Contact)
    allEmployeesGroup.grant_role("Admin", Order)
    allEmployeesGroup.grant_role("Admin", get_class("hourregistrations", "hourregistration"))
    allEmployeesGroup.grant_role("Admin", get_class("announcements", "announcement"))
    allEmployeesGroup.grant_role("Admin", Product)
    allEmployeesGroup.grant_role("Member", Log)
    allEmployeesGroup.grant_role("Member", Supplier)
    allEmployeesGroup.grant_role("Member", Ticket)
    allEmployeesGroup.grant_role("Member", Notification)

    return company, user


def findElementByOldID(elements, id):
    for e in elements:
        if str(e[1]) == str(id):
            return e[0]
    return None


class Command(BaseCommand):
    def migrate_contacts(self, cursor):
        cursor.execute("SELECT * FROM kundebrukere")
        contacts = []
        for cu in cursor.fetchall():
            p = Contact()
            p.full_name = cu['fult_navn'].decode('latin1')
            p.phone = cu['telefon'].decode('latin1')

            if cu['telefon_kontor']:
                p.phone_office = cu['telefon_kontor'].decode('latin1')
            if cu['telefon_mobil']:
                p.phone_mobile = cu['telefon_mobil'].decode('latin1')
            if cu['epostadresse_kundebruker']:
                p.email = cu['epostadresse_kundebruker'].decode('latin1')

            if cu['ansvar']:
                p.description = cu['ansvar'].decode("latin1")

            p.save()
            contacts.append((p, cu['kundebrukerid']))
        return contacts

    def migrate_suppliers(self, cursor):
        print "Migrating suppliers"
        suppliers = []
        cursor.execute("SELECT * FROM leverandor")
        for cu in cursor.fetchall():
            p = Supplier()
            p.name = cu['levnavn'].decode('latin1')
            p.address = cu['adresse'].decode('latin1')
            p.address = p.address.replace("<br/>", "\n")
            p.zip = cu['postnr'].decode("latin1")
            p.phone = cu['telefon'].decode("latin1")
            p.email_contact = cu['kontaktepost'].decode("latin1")
            p.email_order = cu['bestillepost'].decode("latin1")
            p.country = cu['land']

            if cu['vart_kundenr']:
                p.reference = cu['vart_kundenr']

            p.save()
            suppliers.append((p, cu['levid']))

        print "Done migrating suppliers"
        return suppliers

    def migrate_product_categories(self, cursor):
        print "Migrating product categories"
        productcategories = []
        cursor.execute("SELECT * FROM lager_varegrupper")
        for cu in cursor.fetchall():
            p = ProductCategory()
            p.name = cu['varegruppenavn'].decode('latin1')
            p.save()
            productcategories.append((p, cu['varegruppenr']))
        print "Done migrating product categories"
        return productcategories

    def migrate_product_groups(self, cursor, productcategories):
        print "Migrate product groups"

        productgroups = []
        cursor.execute("SELECT * FROM lager_produktgrupper")
        for cu in cursor.fetchall():
            p = ProductGroup()
            p.name = cu['produktgruppenavn'].decode('latin1')
            p.category = findElementByOldID(productcategories, cu['varegruppenr'])
            p.save()
            productgroups.append((p, cu['produktgruppenr']))

        print "Done migrating product groups"
        return productgroups

    def migrate_customers(self, cursor, contacts):
        print "Migrate customers"
        customers = []
        cursor.execute("SELECT * FROM kunder")
        for cu in cursor.fetchall():
            u = Customer()
            u.cid = cu['kundenr']
            u.full_name = cu['kundenavn'].decode('latin1')
            u.email = cu['epostadresse'].decode('latin1')
            u.phone = cu['telefon'].decode('latin1')

            #Visit and delivery
            u.address = cu['leveringsadresse'].decode('latin1')
            u.area_code = cu['levpostnr'].decode('latin1')

            #Invoice
            u.invoice_address = cu['faktadresse'].decode('latin1')
            u.invoice_area_code = cu['faktpostnr'].decode('latin1')

            u.save()

            customers.append((u, cu['kundenr']))

        print "Done migrating customers"
        return customers

    def migrate_users(self, company, cursor, randomCompanyIdentifier):
        print "Migrating users"
        users = []
        cursor.execute("SELECT * FROM brukere")
        for cu in cursor.fetchall():
            u = User()
            u.username = cu['brukernavn'].decode("latin1") + randomCompanyIdentifier
            u.last_name = cu['fult_navn'].decode("latin1").encode("utf-8")
            u.email = cu['epostadresse'].decode("latin1")
            u.phone = cu['telefon']
            u.company = company
            u.save()

            company.allEmployeesGroup.add(u)
            company.save()

            users.append((u, cu['brukerid']))
            
        print "Done migrating users"
        return users


    def migrate_projects(self, company, cursor, users, contacts):
        print "Migrating projects"
        projects = []
        cursor.execute("SELECT * FROM prosjekter")
        for cu in cursor.fetchall():
            p = Project()
            p.pid = cu['prosjektid']
            p.project_name = cu['prosjektnavn'].decode('latin1')
            p.description = cu['beskrivelse'].decode('latin1').replace("<br/>", "\n")
            p.customer = Customer.objects.get(cid=cu['kundenr'], company=company)

            if cu['ansvarlig']:
                p.responsible = findElementByOldID(users, cu['ansvarlig'])

            p.save()

            if cu['kontaktperson']:
                p.contact = findElementByOldID(contacts, cu['kontaktperson'])
                p.save()

                if p.customer:
                    p.customer.contacts.add(findElementByOldID(contacts, cu['kontaktperson']))
                    p.customer.save()

            projects.append((p, cu['prosjektid']))

        return projects

        print "Done migrating projects"

    def migrate_orders(self, company, cursor, users):
        print "Migrating orders"
        cursor.execute("SELECT * FROM ordrer")
        orders = []
        for cu in cursor.fetchall():
            if(len(orders) % 150 == 0):
                print len(orders)

            p = Order()
            p.state = "Order"
            if cu['ordrenr'] and cu['ordrenr'].isdigit():
                p.oid = cu['ordrenr']

            if cu['ordrenavn']:
                p.order_name = cu['ordrenavn'].decode('latin1')

            if cu['ordrebeskrivelse']:
                p.description = cu['ordrebeskrivelse'].decode('latin1').replace("<br/>", "\n")

            if cu['ansvarlig']:
                p.responsible = findElementByOldID(users, cu['ansvarlig'])

            if cu['date_delivery']:
                p.delivery_date = cu['date_delivery']

            if cu['date_delivery_deadline']:
                p.delivery_date_deadline = cu['date_delivery_deadline']

            try:
                p.customer = Customer.objects.get(cid=cu['kundenr'], company=company)
            except:
                pass
            try:
                p.project = Project.objects.get(pid=(cu['prosjektid']), company=company)
            except:
                pass

            p.save()
            orders.append((p, cu['ordrenr']))

        print "Done migrating orders"
        return orders

    def migrate_timetracking(self, cursor, users, orders):
        print "Migrating timetracking"
        cursor.execute("SELECT * FROM timereg")

        timetrackings = []

        for cu in cursor.fetchall():
            user = findElementByOldID(users, str(cu['brukerid']))
            Core.set_test_user(user)

            if(len(timetrackings) % 150 == 0):
                print len(timetrackings)

            o = HourRegistration()
            o.order = findElementByOldID(orders, str(cu['ordrenr']))

            if(cu['date']):
                o.date = cu['date']

            o.time_start = "08:00"
            end_time = datetime.strptime("2010-10-10 08:00:00", "%Y-%m-%d %H:%M:%S") + timedelta(
                hours=(float((cu['antalltimer_totalt'].decode("latin1")))))

            o.time_end = end_time.strftime("%H:%M")

            try:
                o.description = cu['beskrivelse_time'].decode("latin1")
            except:
                pass
            
            try:
                o.save()
                timetrackings.append(o)
            except:
                pass
        print "Done migrating timetracking"

        return timetrackings

    def migrate_products(self, cursor, productgroups, suppliers):
        print "Migrating products"

        cursor.execute("SELECT * FROM lager_varer")
        for cu in cursor.fetchall():
            p = Product()
            if cu['varenr']:
                p.pid = cu['varenr'].decode("latin1")

            p.size = 0
            p.price_in = (cu['pris_inn'])
            p.max_discount = (cu['maks_avslag'])
            p.price = (cu['pris'])
            p.unitForSize = UnitsForSizes.objects.get_or_create(name=cu['prisenhet'].decode('latin1'))[0]
            p.priceVal = Currency.objects.get_or_create(name=cu['prisenhet'].decode('latin1'))[0]
            p.name = cu['varenavn'].decode('latin1')
            p.description = cu['varebetegnelse'].decode("latin1")

            #Foreign keys
            p.supplier = findElementByOldID(suppliers, int(cu['levid']))
            p.productGroup = findElementByOldID(productgroups, cu['produktgruppenr'])

            p.save()
        print "Done migrating products"

    def connect_database(self):
        conn = MySQLdb.connect(host="focustimeno.mysql.domeneshop.no",
                               user="focustimeno",
                               passwd="XFu7qBLy",
                               db="focustimeno",
                               cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        return cursor

    def handle(self, *apps, **options):
        print "======================================================="

        print "Connecting to database..."
        cursor = self.connect_database()

        print "Connection established!"

        randomCompanyIdentifier = str(int(random.random() * 99999))

        company, user = createNewCustomer("Ledere", "Bjarte Hatlenes", "superadmin",
                                          "superadmin" + randomCompanyIdentifier, "Ansatte",
                                          "Focus Security AS")

        Core.set_test_user(user)
        generate_new_password_for_user(user)

        print "Company: %s " % company
        print "Current user is: %s " % Core.current_user()

        users = self.migrate_users(company, cursor, randomCompanyIdentifier)

        contacts = self.migrate_contacts(cursor)

        self.migrate_customers(cursor, contacts)

        self.migrate_projects(company, cursor, users, contacts)

        orders = self.migrate_orders(company, cursor, users)

        self.migrate_timetracking(cursor, users, orders)

        #Set test user again
        Core.set_test_user(user)

        suppliers = self.migrate_suppliers(cursor)

        productcategories = self.migrate_product_categories(cursor)

        productgroups = self.migrate_product_groups(cursor, productcategories)

        self.migrate_products(cursor, productgroups, suppliers)

        """

        TODO: ADD CONTACTS TO PROJECT
        TODO: ADD CONTACTS TO CUSTOMER
        TODO: ADD CONTACTS TO ORDER

        """

        print "Done!"


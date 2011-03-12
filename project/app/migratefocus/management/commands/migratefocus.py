# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from django.core.management.base import BaseCommand
import os
import MySQLdb
import MySQLdb.cursors
from core import Core
from core.models import User, Group, Company, Log, Notification
import random
from app.admin.views.user import generateNewPassordForUser

def getClass(app, model):
    content_type = ContentType.objects.get(app_label=app, model=model)
    model = content_type.model_class()
    return model

Customer = getClass("customers", "customer")
Project = getClass("projects", "project")
Order = getClass("orders", "order")
Supplier = getClass("suppliers", "supplier")
Contact = getClass("contacts", "contact")
Product = getClass("stock", "product")
UnitsForSizes = getClass("stock", "unitsforsizes")
Currency = getClass("stock", "currency")
ProductCategory = getClass("stock", "productcategory")
ProductGroup = getClass("stock", "productgroup")

def createNewCustomer(adminGroup, adminuserName, adminuserPassword, adminuserUsername, allEmployeesGroup, name):
    adminGroup = Group(name=adminGroup)
    adminGroup.saveWithoutCreatePermissions()
    allEmployeesGroup = Group(name=allEmployeesGroup)
    allEmployeesGroup.saveWithoutCreatePermissions()
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
    adminGroup.addMember(user)
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
    adminGroup.grant_role("Admin", getClass("hourregistrations", "hourregistration"))
    adminGroup.grant_role("Admin", getClass("announcements", "announcement"))
    adminGroup.grant_role("Admin", Product)
    adminGroup.grant_role("Admin", Log)
    adminGroup.grant_role("Admin", Supplier)
    adminGroup.grant_role("Admin", Notification)
    adminGroup.grant_role("Admin", User)
    adminGroup.grant_role("Admin", Group)
    adminGroup.grant_permissions("CONFIGURE", Company)
    #Give employee group some permissions on classes
    allEmployeesGroup.grant_role("Admin", Project)
    allEmployeesGroup.grant_role("Admin", Customer)
    allEmployeesGroup.grant_role("Admin", Contact)
    allEmployeesGroup.grant_role("Admin", Order)
    allEmployeesGroup.grant_role("Admin", getClass("hourregistrations", "hourregistration"))
    allEmployeesGroup.grant_role("Admin", getClass("announcements", "announcement"))
    allEmployeesGroup.grant_role("Admin", Product)
    allEmployeesGroup.grant_role("Member", Log)
    allEmployeesGroup.grant_role("Member", Supplier)
    allEmployeesGroup.grant_role("Member", Notification)

    return company, user

def findElementByOldID(users, oldID):
    for user in users:
        if user[1] == oldID:
            return user[0]
    return None

class Command(BaseCommand):
    def migrate_contacts(self, cursor):
        cursor.execute("SELECT * FROM kundebrukere")
        for cu in cursor.fetchall():
            p = Contact()
            p.full_name = cu['fult_navn'].decode('latin1')
            p.phone = cu['telefon'].decode('latin1')
            p.email = cu['epostadresse_kundebruker'].decode('latin1')
            p.save()

    def migrate_suppliers(self, cursor):
        suppliers = []
        cursor.execute("SELECT * FROM leverandor")
        for cu in cursor.fetchall():
            p = Supplier()
            p.name = cu['levnavn'].decode('latin1')
            p.address = cu['adresse'].decode('latin1')
            p.save()
            suppliers.append((p, cu['levid']))
        print "suppliers: %s" % suppliers
        return suppliers

    def migrate_product_categories(self, cursor):
        productcategories = []
        cursor.execute("SELECT * FROM lager_varegrupper")
        for cu in cursor.fetchall():
            p = ProductCategory()
            p.name = cu['varegruppenavn'].decode('latin1')
            p.save()
            productcategories.append((p, cu['varegruppenr']))
        print "productcategories %s " % productcategories
        return productcategories

    def migrate_product_groups(self, cursor, productcategories):
        productgroups = []
        cursor.execute("SELECT * FROM lager_produktgrupper")
        for cu in cursor.fetchall():
            p = ProductGroup()
            p.name = cu['produktgruppenavn'].decode('latin1')
            p.category = findElementByOldID(productcategories, cu['varegruppenr'])
            p.save()
            productgroups.append((p, cu['produktgruppenr']))
        return productgroups

    def migrate_customers(self, cursor):
        cursor.execute("SELECT * FROM kunder")
        for cu in cursor.fetchall():
            u = Customer()
            u.cid = cu['kundenr']
            u.full_name = cu['kundenavn'].decode('latin1')
            u.email = cu['epostadresse'].decode('latin1')
            u.phone = cu['telefon'].decode('latin1')
            u.address = cu['leveringsadresse'].decode('latin1')
            u.area_code = cu['levpostnr'].decode('latin1')
            u.save()

    def migrate_users(self, company, cursor, randomCompanyIdentifier, users):
        for cu in cursor.fetchall():
            u = User()
            u.username = cu['brukernavn'].decode("latin1") + randomCompanyIdentifier
            u.last_name = cu['fult_navn'].decode("latin1").encode("utf-8")
            u.email = cu['epostadresse'].decode("latin1")
            u.phone = cu['telefon']
            u.company = company
            u.save()
            users.append((u, cu['brukerid']))

    def migrate_projects(self, company, cursor):
        cursor.execute("SELECT * FROM prosjekter")
        for cu in cursor.fetchall():
            p = Project()
            p.pid = cu['prosjektid']
            p.project_name = cu['prosjektnavn'].decode('latin1')
            p.description = cu['beskrivelse'].decode('latin1')
            p.customer = Customer.objects.get(cid=cu['kundenr'], company=company)
            p.save()

    def migrate_orders(self, company, cursor, users):
        cursor.execute("SELECT * FROM ordrer")
        for cu in cursor.fetchall():
            p = Order()
            p.state = "Order"
            if cu['ordrenr'] and cu['ordrenr'].isdigit():
                p.oid = cu['ordrenr']

            if cu['ordrenavn']:
                p.order_name = cu['ordrenavn'].decode('latin1')

            if cu['ordrebeskrivelse']:
                p.description = "OK"

            if cu['ansvarlig']:
                p.responsible = findElementByOldID(users, cu['ansvarlig'])

            try:
                p.customer = Customer.objects.get(cid=cu['kundenr'], company=company)
                p.project = Project.objects.get(pid=(cu['prosjektid']), company=company)
            except:
                pass

            p.save()

    def migrate_products(self, cursor, productgroups, suppliers):
        cursor.execute("SELECT * FROM lager_varer")
        for cu in cursor.fetchall():
            p = Product()
            if cu['varenr']:
                p.pid = cu['varenr'].decode("latin1")

            p.size = 0
            p.unitForSize = UnitsForSizes.objects.get_or_create(name=cu['prisenhet'].decode('latin1'))[0]
            p.supplier = findElementByOldID(suppliers, cu['levid'])
            p.priceVal = Currency.objects.get_or_create(name=cu['prisenhet'].decode('latin1'))[0]
            p.name = cu['varenavn'].decode('latin1')
            p.description = cu['varebetegnelse'].decode("latin1")
            p.productGroup = findElementByOldID(productgroups, cu['produktgruppenr'])
            p.save()

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
        generateNewPassordForUser(user)

        print "Company: %s " % company
        print "Current user is: %s " % Core.current_user()

        print "Migrate users"

        users = []

        cursor.execute("SELECT * FROM brukere")
        self.migrate_users(company, cursor, randomCompanyIdentifier, users)

        print "Migrate customers"
        #self.migrate_customers(cursor)

        print "Migrate projects"
        #self.migrate_projects(company, cursor)

        print "Migrate orders"
        #self.migrate_orders(company, cursor, users)

        print "Migrate contacts"
        #self.migrate_contacts(cursor)

        print "Migrate suppliers"
        suppliers = self.migrate_suppliers(cursor)

        print "Migrate product categories"
        productcategories = self.migrate_product_categories(cursor)

        print "Migrate product groups"
        productgroups = self.migrate_product_groups(cursor, productcategories)

        print "Migrate products"
        self.migrate_products(cursor, productgroups, suppliers)

        print "Done!"


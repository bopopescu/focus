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

class Command(BaseCommand):
    def handle(self, *apps, **options):
        conn = MySQLdb.connect(host="focustimeno.mysql.domeneshop.no",
                               user="focustimeno",
                               passwd="XFu7qBLy",
                               db="focustimeno",
                               cursorclass=MySQLdb.cursors.DictCursor)

        cursor = conn.cursor()

        print "======================================================="

        print "Create new company"

        company, user = createNewCustomer("Ledere", "Bjarte Hatlenes", "superadmin",
                                          "bjarte" + str(int(random.random() * 99999)), "Ansatte",
                                          "Focus Security AS")

        Core.set_test_user(user)
        generateNewPassordForUser(user)

        print "Current user is: %s " % Core.current_user()

        print "Migrate users"

        cursor.execute("SELECT * FROM brukere")
        for cu in cursor.fetchall():
            u = User()
            u.focusID = cu['brukerid']
            u.username = cu['brukernavn'].decode("latin1") + str(int(random.random() * 99999))
            u.last_name = cu['fult_navn'].decode("latin1")
            u.email = cu['epostadresse'].decode("latin1")
            u.phone = cu['telefon']
            u.company = company
            u.save()

        print "Migrate customers"

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

        print "Migrate projects"

        cursor.execute("SELECT * FROM prosjekter")
        for cu in cursor.fetchall():
            p = Project()
            p.pid = cu['prosjektid']
            p.project_name = cu['prosjektnavn'].decode('latin1')
            p.description = cu['beskrivelse'].decode('latin1')
            p.customer = Customer.objects.get(cid=cu['kundenr'], company=company)
            p.save()

        print "Migrate orders"
        cursor.execute("SELECT * FROM ordrer")
        for cu in cursor.fetchall():
            p = Order()
            p.state = "Order"
            if cu['ordrenr'] and cu['ordrenr'].isdigit():
                p.oid = cu['ordrenr']

            if cu['ordrenavn']:
                p.order_name = cu['ordrenavn'].decode('latin1')

            if cu['ordrebeskrivelse']:
                p.description = cu['ordrebeskrivelse'].decode('latin1')

            if cu['ansvarlig']:
                p.responsible = User.objects.get(focusID=cu['ansvarlig'], company=company)

            try:
                p.customer = Customer.objects.get(cid=cu['kundenr'], company=company)
                p.project = Project.objects.get(pid=(cu['prosjektid']), company=company)
            except:
                pass

            p.save()

        print "Migrate suppliers"
        cursor.execute("SELECT * FROM leverandor")
        for cu in cursor.fetchall():
            p = Supplier()
            p.name = cu['levnavn'].decode('latin1')
            p.address = cu['adresse'].decode('latin1')
            p.save()

        print "Migrate contacts"
        cursor.execute("SELECT * FROM kundebrukere")
        for cu in cursor.fetchall():
            p = Contact()
            p.full_name = cu['fult_navn'].decode('latin1')
            p.phone = cu['telefon'].decode('latin1')
            p.email = cu['epostadresse_kundebruker'].decode('latin1')
            p.save()

        print "Migrate products"
        cursor.execute("SELECT * FROM lager_varer")
        for cu in cursor.fetchall():
            p = Product()
            if cu['varenr']:
                p.pid = cu['varenr'].decode("latin1")

            p.name = cu['varenavn'].decode('latin1')
            p.description = cu['varebetegnelse'].decode("latin1")
            p.save()



from app.announcements.models import Announcement
from app.company.forms import CompanyForm, newCompanyForm
from app.contacts.models import Contact
from app.customers.models import Customer
from app.orders.models import Order
from app.projects.models import Project
from app.hourregistrations.models import HourRegistration
from app.stock.models import Product
from core.shortcuts import *
from core.decorators import *
from core.views import updateTimeout
from core.auth.company.models import Company
from core.auth.user.models import User
from core.auth.group.models import Group
from core.auth.log.models import Log, Notification


@require_permission("MANAGE", Company)
def overview(request):
    updateTimeout(request)
    companies = Company.objects.all()

    return render_with_request(request, 'company/list.html', {'title': 'Firmaer',
                                                              'companies': companies})


@require_permission("MANAGE", Company)
def add(request):
    return newForm(request)


@require_permission("MANAGE", Company)
def edit(request, id):
    return form(request, id)


def form (request, id=False):
    if id:
        instance = Company.objects.all().get(id=id)
        msg = "Velykket endret kunde"
    else:
        instance = Company()
        msg = "Velykket lagt til ny kunde"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            request.message_success(msg)

            return redirect(overview)
    else:
        form = CompanyForm(instance=instance)

    return render_with_request(request, "company/form.html", {'title': 'Kunde', 'form': form})


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
    adminGroup.grant_role("Admin", HourRegistration)
    adminGroup.grant_role("Admin", Announcement)
    adminGroup.grant_role("Admin", Log)
    adminGroup.grant_role("Admin", Product)
    adminGroup.grant_role("Admin", Notification)
    adminGroup.grant_role("Admin", User)
    adminGroup.grant_role("Admin", Group)
    adminGroup.grant_permissions("CONFIGURE", Company)
    #Give employee group some permissions on classes
    allEmployeesGroup.grant_role("Member", Project)
    allEmployeesGroup.grant_role("Member", Customer)
    allEmployeesGroup.grant_role("Member", Contact)
    allEmployeesGroup.grant_role("Member", HourRegistration)
    allEmployeesGroup.grant_role("Member", Product)
    allEmployeesGroup.grant_role("Member", Order)
    allEmployeesGroup.grant_role("Member", Announcement)
    allEmployeesGroup.grant_role("Member", Log)
    allEmployeesGroup.grant_role("Member", Notification)
    #Manually give som other permissions
    allEmployeesGroup.grant_permissions("CREATE", HourRegistration)
    #Manually give som other permissions
    allEmployeesGroup.grant_permissions("CREATE", Contact)

    return company, user


@require_permission("MANAGE", Company)
def newForm(request):
    if request.method == 'POST': # If the form has been submitted...
        form = newCompanyForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            name = form.cleaned_data['name']
            adminGroup = form.cleaned_data['adminGroup']
            allEmployeesGroup = form.cleaned_data['allEmployeesGroup']
            adminuserName = form.cleaned_data['adminuserName']
            adminuserUsername = form.cleaned_data['adminuserUsername']
            adminuserPassword = form.cleaned_data['adminuserPassword']

            createNewCustomer(adminGroup, adminuserName, adminuserPassword, adminuserUsername, allEmployeesGroup, name)

            return redirect(overview)
    else:
        form = newCompanyForm() # An unbound form

    return render_with_request(request, "company/form.html", {'title': 'Nytt firma', 'form': form})

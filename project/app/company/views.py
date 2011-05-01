from app.announcements.models import Announcement
from app.company.forms import CompanyForm, newCompanyForm
from app.contacts.models import Contact
from app.customers.models import Customer
from app.orders.models import Order
from app.projects.models import Project
from app.hourregistrations.models import HourRegistration
from app.stock.models import Product
from core.decorators import require_permission
from core.views import update_timeout
from core.auth.company.models import Company
from core.auth.user.models import User
from core.auth.group.models import Group
from core.auth.log.models import Log, Notification
from django.shortcuts import render, redirect


@require_permission("MANAGE", Company)
def overview(request):
    update_timeout(request)
    companies = Company.objects.all()

    return render(request, 'company/list.html', {'title': 'Firmaer',
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

    return render(request, "company/form.html", {'title': 'Kunde', 'form': form})

def createNewCustomer(data):
    admin_group = Group(name=data['admin_group'])
    admin_group.save_without_permissions()
    all_employees_group = Group(name=data['all_employees_group'])
    all_employees_group.save_without_permissions()
    company = Company(name=data['name'], admin_group=admin_group, all_employees_group=all_employees_group)

    #Set up email for receiving tickets
    company.email_address = data['email_address']
    company.email_host = data['email_host']
    company.email_password = data['email_password']
    company.email_username = data['email_username']

    company.save()

    #Create the admin user
    user = User(first_name=data['adminuser_name'], username=data['adminuser_username'])
    user.set_password(data['adminuser_password'])
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
    admin_group.grant_role("Admin", Order)
    admin_group.grant_role("Admin", HourRegistration)
    admin_group.grant_role("Admin", Announcement)
    admin_group.grant_role("Admin", Log)
    admin_group.grant_role("Admin", Product)
    admin_group.grant_role("Admin", Notification)
    admin_group.grant_role("Admin", User)
    admin_group.grant_role("Admin", Group)
    admin_group.grant_permissions("CONFIGURE", Company)

    #Give employee group some permissions on classes
    all_employees_group.grant_role("Member", Project)
    all_employees_group.grant_role("Member", Customer)
    all_employees_group.grant_role("Member", Contact)
    all_employees_group.grant_role("Member", HourRegistration)
    all_employees_group.grant_role("Member", Product)
    all_employees_group.grant_role("Member", Order)
    all_employees_group.grant_role("Member", Announcement)
    all_employees_group.grant_role("Member", Log)
    all_employees_group.grant_role("Member", Notification)
    #Manually give som other permissions
    all_employees_group.grant_permissions("CREATE", HourRegistration)
    #Manually give som other permissions
    all_employees_group.grant_permissions("CREATE", Contact)

    return company, user

@require_permission("MANAGE", Company)
def newForm(request):
    if request.method == 'POST': # If the form has been submitted...
        form = newCompanyForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            data = form.cleaned_data
            createNewCustomer(data)

            return redirect(overview)
    else:
        form = newCompanyForm() # An unbound form

    return render(request, "company/form.html", {'title': 'Nytt firma', 'form': form})

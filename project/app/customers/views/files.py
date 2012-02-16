from django.shortcuts import render, redirect, get_object_or_404
from app.files.forms import FileForm
from app.files.models import File
from app.files.views import generic_form as file_form
from app.customers.models import Customer
from core import Core
from core.decorators import require_permission

@require_permission("VIEW", Customer, 'id')
def overview(request, id):
    """
    id is customer_id
    """
    customer = Core.current_user().get_permitted_objects("VIEW", Customer).all().get(id=id)

    #Set URL for edit for files in customer
    edit_file_url = "/customers/%s/files/" % customer.id

    return render(request, "customers/files/list.html",
            {'customer': customer,
             'file_manager': customer,
             'edit_file_url': edit_file_url})


@require_permission("VIEW", Customer, 'id')
def add_file(request, id):
    """
    id = customer_id
    """
    customer = Core.current_user().get_permitted_objects("VIEW", Customer).all().get(id=id)
    file = File()

    additional_data = {'customer': customer}


    return file_form(request, customer, file, redirect(overview, id), additional_data,
                     template="customers/files/form.html")


@require_permission("VIEW", Customer, 'id')
def edit_file(request, id, file_id):
    """
    id = customer_id
    file_id = file_id
    """
    customer = Core.current_user().get_permitted_objects("VIEW", Customer).all().get(id=id)
    file = customer.files.get(id=file_id)

    additional_data = {'customer': customer}

    return file_form(request, customer, file, redirect(overview, id), additional_data,
                     template="customers/files/form.html")
from django.shortcuts import render, redirect, get_object_or_404
from app.files.forms import FileForm
from app.files.models import File
from app.files.views import generic_form as file_form
from app.orders.models import Order
from core import Core
from core.decorators import require_permission

@require_permission("VIEW", Order, 'id')
def overview(request, id):
    """
    id is order_id
    """
    order = Core.current_user().get_permitted_objects("VIEW", Order).all().get(id=id)

    #Set URL for edit for files in order
    edit_file_url = "/orders/%s/files/" % order.id

    return render(request, "orders/files/list.html",
            {'order': order,
             'file_manager': order,
             'edit_file_url': edit_file_url})


@require_permission("VIEW", Order, 'id')
def add_file(request, id):
    """
    id = order_id
    """
    order = Core.current_user().get_permitted_objects("VIEW", Order).all().get(id=id)
    file = File()

    additional_data = {'order': order}

    return file_form(request, order, file, redirect(overview, id), additional_data, template="orders/files/form.html")


@require_permission("VIEW", Order, 'id')
def edit_file(request, id, file_id):
    """
    id = order_id
    file_id = file_id
    """
    order = Core.current_user().get_permitted_objects("VIEW", Order).all().get(id=id)
    file = order.files.get(id=file_id)
    additional_data = {'order': order}

    return file_form(request, order, file, redirect(overview, id), additional_data, template="orders/files/form.html")
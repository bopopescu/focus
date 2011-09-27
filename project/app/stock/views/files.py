from django.shortcuts import render, redirect, get_object_or_404
from app.files.forms import FileForm
from app.files.models import File
from app.files.views import generic_form as file_form
from app.stock.models import Product
from core import Core
from core.decorators import login_required

def overview(request, id):
    """
    id is project_id
    """
    instance = Core.current_user().get_permitted_objects("VIEW", Product).all().get(id=id)

    #Set URL for edit for files in project
    edit_file_url = "/stock/product/%s/files/" % instance.id

    return render(request, "stock/files/list.html",
                                                        {'product': instance,
                                                         'file_manager': instance,
                                                         'edit_file_url': edit_file_url})

@login_required()
def add_file(request, id):
    """
    id = project_id
    """
    instance = Core.current_user().get_permitted_objects("VIEW", Product).all().get(id=id)
    file = File()

    additional_data = {'product': instance}

    return file_form(request, instance, file, redirect(overview, id), additional_data,
                     template="stock/files/form.html")



@login_required()
def edit_file(request, id, file_id):
    """
    id = project_id
    file_id = file_id
    """
    instance = Core.current_user().get_permitted_objects("VIEW", Product).all().get(id=id)
    file = instance.files.get(id=file_id)
    additional_data = {'product': instance}

    return file_form(request, instance, file, redirect(overview, id), additional_data,
                     template="stock/files/form.html")
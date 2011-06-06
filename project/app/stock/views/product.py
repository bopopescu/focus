# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect, render
from core import Core
from core.decorators import require_permission
from core.utils import suggest_ajax_parse_arguments
from core.views import  update_timeout
from app.stock.forms import ProductForm, ProductFileForm
from app.stock.models import Product, ProductFile
from django.utils.simplejson import JSONEncoder
from django.http import HttpResponse
from django.db.models.query_utils import Q
from django.utils.translation import ugettext as _

@require_permission("LIST", Product)
def overview(request):
    update_timeout(request)
    #products = Product.objects.filter(trashed=False)
    products = Core.current_user().get_permitted_objects("VIEW", Product)

    return render(request, 'stock/products/list.html', {'title': _("Products"), 'products': products})


@require_permission("LISTDELETED", Product)
def overview_trashed(request):
    update_timeout(request)
    products = Product.objects.filter(trashed=True)
    return render(request, 'stock/products/list.html', {'title': _("Products"), 'products': products})


@require_permission("CREATE", Product)
def add(request):
    return form(request)


@require_permission("EDIT", Product, "id")
def edit(request, id):
    return form(request, id)


@require_permission("EDIT", Product, "id")
def orders(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'stock/products/orders.html',
                  {'title': _("Product used in these orders"), 'product': product,
                   'orders': product.orders})


@require_permission("EDIT", Product, "id")
def files(request, id):
    product = Product.objects.get(id=id)
    productFileForm = ProductFileForm(instance=ProductFile())
    files = product.files.filter(parent=None)
    
    return render(request, 'stock/products/files.html',
                  {'title': _("Files"), 'product': product,
                   'productFileForm': productFileForm,
                   'files': files})


@require_permission("EDIT", Product, "id")
def addFile(request, id):
    instance = ProductFile()

    if request.method == 'POST':
        form = ProductFileForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            product = Product.objects.get(id=id)
            o = form.save(commit=False)
            o.product = product
            o.save()
            request.message_success(_("Successfully uploaded file"))

            return redirect(files, id)

        request.message_error(_("Invalid file"))

        return redirect(files, id)

    else:
        request.message_error(_("An error occoured"))
        return redirect(files, id)

@require_permission("EDIT", Product, "id")
def replaceFile (request, id, fileID):

    product = get_object_or_404(Product, id=id, deleted=False)
    
    instance = get_object_or_404(ProductFile, id=fileID, deleted=False)
    clone = instance.clone()

    #Save and set to active
    if request.method == 'POST':
        form = ProductFileForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            clone.parent = o
            clone.save()

            #Redirects for direct editing
            return redirect(replaceFile, id, fileID)

    else:
        form = ProductFileForm(instance=instance, initial={"file": None})

    file_history = instance.get_history()

    return render(request, 'stock/products/files_form.html', {'title': "Endre fil",
                                        'form': form,
                                        'file':instance,
                                        'file_history':file_history})


@require_permission("EDIT", Product, "id")
def deleteFile(request, id, fileID):
    product = get_object_or_404(Product, id=id, deleted=False)
    file = product.files.get(id=fileID)
    file.delete()

    return redirect(files, id)


@require_permission("DELETE", Product, "id")
def trash(request, id):
    instance = Product.objects.get(id=id)

    if request.method == "POST":
        if not instance.can_be_deleted()[0]:
            request.message_error("You can't delete this product because: ")
            for reason in instance.can_be_deleted()[1]:
                request.message_error(reason)
        else:
            request.message_success("Successfully trashed this product")
            instance.trash()
        return redirect(overview)
    else:
        return render(request, 'stock/products/trash.html', {'title': _("Confirm delete"),
                                                             'product': instance,
                                                             'can_be_deleted': instance.can_be_deleted()[0],
                                                             'reasons': instance.can_be_deleted()[1],
                                                             })


@require_permission("DELETE", Product, "id")
def recover(request, id):
    Product.objects.get(id=id).recover()
    return redirect(overview)


@suggest_ajax_parse_arguments()
def autocomplete(request, query, limit):
    products = Product.objects.filter(
        Q(name__startswith=query)
    )[:limit]

    products = [{'id': product.id,
                 'label': "%s" % (product.name),
                 'value': product.name} for product in products]

    return HttpResponse(JSONEncoder().encode(products), mimetype='application/json')


@require_permission("VIEW", Product, "id")
def view(request, id):
    instance = ProductFile()
    product = Product.objects.get(id=id)

    return render(request, 'stock/products/view.html', {'title': _("Product"),
                                                        'product': product,
                                                        })


def form (request, id=False):
    if id:
        instance = get_object_or_404(Product, id=id, deleted=False)
        msg = _("Successfully edited product")
        pid = instance.pid
    else:
        instance = Product()
        instance.pid = Product.calculate_next_pid()
        pid =  Product.calculate_next_pid()

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            request.message_success(msg)

            return redirect(view, o.id)

    else:
        form = ProductForm(instance=instance)

    return render(request, "stock/form.html", {'title': _("Product"),
                                               'product': instance,
                                               'form': form})
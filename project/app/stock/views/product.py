# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from core.shortcuts import *
from core.decorators import require_permission
from core.views import  updateTimeout
from app.stock.forms import ProductForm, ProductFileForm
from app.stock.models import Product, ProductFile
from django.utils.translation import ugettext as _

@require_permission("LIST", Product)
def overview(request):
    updateTimeout(request)
    products = Product.objects.all()

    return render_with_request(request, 'stock/products/list.html', {'title': _("Products"), 'products': products})

@require_permission("LISTDELETED", Product)
def overview_trashed(request):
    updateTimeout(request)
    products = Product.objects.filter(deleted=True)
    return render_with_request(request, 'stock/products/list.html', {'title': _("Products"), 'products': products})

@require_permission("CREATE", Product)
def add(request):
    return form(request)

@require_permission("EDIT", Product, "id")
def edit(request, id):
    return form(request, id)

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

            return redirect(view, id)

        request.message_error(_("Invalid file"))

        return redirect(edit, id)

    else:
        request.message_error(_("An error occoured"))
        return redirect(overview)

@require_permission("EDIT", Product, "id")
def deleteFile(request, id, fileID):
    product = get_object_or_404(Product, id=id, deleted=False)
    file = product.files.get(id=fileID)
    file.delete()

    return redirect(view, id)

@require_permission("DELETE", Product, "id")
def delete(request, id):
    Product.objects.get(id=id).delete()
    return redirect(overview)

@require_permission("DELETE", Product, "id")
def recover(request, id):
    Product.objects.get(id=id).recover()
    return redirect(overview)

@require_permission("VIEW", Product, "id")
def view(request, id):
    instance = ProductFile()
    productFileForm = ProductFileForm(instance=instance)
    product = Product.objects.get(id=id)

    return render_with_request(request, 'stock/products/view.html', {'title': _("Product"),
                                                                     'product': product,
                                                                     'productFileForm': productFileForm})

def form (request, id=False):
    if id:
        instance = get_object_or_404(Product, id=id, deleted=False)
        msg = _("Successfully edited product")
    else:
        instance = Product()
        msg = _("Successfully added product")

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            request.message_success(msg)

            return redirect(overview)

    else:
        form = ProductForm(instance=instance)

    return render_with_request(request, "stock/form.html", {'title': _("Product"),
                                                            'product': instance,
                                                            'form': form})
# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from core.shortcuts import *
from core.decorators import require_permission
from core.views import  updateTimeout
from app.stock.forms import ProductForm
from app.stock.models import Product

@require_permission("LIST", Product)
def overview(request):
    updateTimeout(request)
    products = Product.objects.all()

    return render_with_request(request, 'stock/products/list.html', {'title': 'Produkter', 'products': products})

@require_permission("LISTDELETED", Product)
def overview_deleted(request):
    updateTimeout(request)
    products = Product.objects.filter(deleted=True)
    return render_with_request(request, 'stock/products/list.html', {'title': 'Produkter', 'products': products})

@require_permission("CREATE", Product)
def add(request):
    return form(request)

@require_permission("EDIT", Product, "id")
def edit(request, id):
    return form(request, id)

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
    product = Product.objects.get(id=id)
    return render_with_request(request, 'stock/products/view.html', {'title': 'Produkt', 'product': product})

def form (request, id=False):
    if id:
        instance = get_object_or_404(Product, id=id, deleted=False)
        msg = "Velykket endret produkt"
    else:
        instance = Product()
        msg = "Velykket lagt til nytt produkt"

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

    return render_with_request(request, "form.html", {'title': 'Produkt', 'form': form})
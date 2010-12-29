# -*- coding: utf-8 -*-

from core.shortcuts import *
from core.decorators import *
from core.views import  updateTimeout
from app.stock.forms import ProductForm
from app.stock.models import Product

@login_required()
def overview(request):
    updateTimeout(request)
    products = Product.objects.for_company()

    return render_with_request(request, 'stock/products/list.html', {'title': 'Produkter', 'products': products})

@login_required()
def overview_deleted(request):
    updateTimeout(request)
    products = Product.objects.for_company(deleted=True)
    return render_with_request(request, 'stock/products/list.html', {'title': 'Produkter', 'products': products})

@login_required()
def add(request):
    return form(request)

def edit(request, id):
    return form(request, id)

def delete(request, id):
    Product.objects.get(id=id).delete()
    return redirect(overview)

def recover(request, id):
    Product.objects.get(id=id).recover()
    return redirect(overview)

def view(request, id):
    product = Product.objects.get(id=id)
    return render_with_request(request, 'stock/products/view.html', {'title': 'Produkt', 'product': product})

@login_required()
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
            messages.success(request, msg)

            return redirect(overview)

    else:
        form = ProductForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Produkt', 'form': form})
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from core.shortcuts import *
from core.decorators import *
from core.views import form_perm, updateTimeout
from app.stock.forms import ProductForm
from app.stock.models import Product

@login_required
def overview(request):
    updateTimeout(request)
    projects = Project.objects.for_user()
    return render_with_request(request, 'stock/products/list.html', {'title':'Produkter', 'projects':projects})

@login_required
def add(request):
    return form(request)

@require_perm('change', Project)
def edit(request, id):
    return form(request, id)

@require_perm('delete', Project)
def delete(request, id):
    Project.objects.get(id=id).delete()
    return redirect(overview)

@login_required
def form (request, id = False):

    if id:
        instance = get_object_or_404(Project, id = id, deleted=False)
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

    return render_with_request(request, "form.html", {'title':'Produkt', 'form': form })
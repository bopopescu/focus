# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import simplejson
from core.shortcuts import render_with_request
from core.decorators import require_permission, login_required
from core.views import  updateTimeout
from app.stock.forms import ProductGroupForm
from app.stock.models import ProductGroup
from django.utils.translation import ugettext as _

@login_required()
def overview(request):
    updateTimeout(request)
    productgroups = ProductGroup.objects.all()
    return render_with_request(request, 'stock/productgroups/list.html',
                               {'title': 'Produktgrupper', 'productgroups': productgroups})

@login_required()
def add(request):
    return form(request)

@login_required()
def edit(request, id):
    return form(request, id)

@login_required()
def delete(request, id):
    ProductGroup.objects.get(id=id).delete()
    return redirect(overview)

@require_permission("CREATE", ProductGroup)
def add_ajax(request):
    form = ProductGroupForm(request.POST, instance=ProductGroup())

    if form.is_valid():
        a = form.save()

        return HttpResponse(simplejson.dumps({'name': a.name,
                                              'valid':True,
                                              'id': a.id}), mimetype='application/json')


    else:
       errors = dict([(field, errors[0]) for field, errors in form.errors.items()])

       return HttpResponse(simplejson.dumps({'errors': errors,
                                             'valid': False}), mimetype='application/json')

    return HttpResponse("ERROR")

@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(ProductGroup, id=id, deleted=False)
        msg = "Velykket endret produktgruppen"
    else:
        instance = ProductGroup()
        msg = "Velykket lagt til ny produktgruppe"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = ProductGroupForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            request.message_success(msg)

            return redirect(overview)

    else:
        form = ProductGroupForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Produktgruppe', 'form': form})
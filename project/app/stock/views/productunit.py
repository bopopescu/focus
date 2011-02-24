# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from app.projects.models import Project
from core.shortcuts import *
from core.decorators import *
from core.views import  updateTimeout
from app.stock.forms import UnitsForSizesForm
from app.stock.models import UnitsForSizes
from django.utils import simplejson
from django.utils.translation import ugettext as _

@login_required()
def overview(request):
    updateTimeout(request)
    units = UnitsForSizes.objects.all()
    return render_with_request(request, 'stock/productUnits/list.html', {'title': 'Enheter', 'units': units})

@login_required()
def add(request):
    return form(request)

def edit(request, id):
    return form(request, id)

def delete(request, id):
    Project.objects.get(id=id).delete()
    return redirect(overview)

@require_permission("CREATE", UnitsForSizes)
def add_ajax(request):
    form = UnitsForSizesForm(request.POST, instance=UnitsForSizes())

    if form.is_valid():
        a = form.save()

        return HttpResponse(simplejson.dumps({'name': a.name,
                                              'id': a.id}), mimetype='application/json')

    return HttpResponse("ERROR")

@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(UnitsForSizes, id=id, deleted=False)
        msg = "Velykket endret enhet"
    else:
        instance = UnitsForSizes()
        msg = "Velykket lagt til ny enhet"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = UnitsForSizesForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            request.message_success(msg)

            return redirect(overview)

    else:
        form = UnitsForSizesForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Enhet', 'form': form})
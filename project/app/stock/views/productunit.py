# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from app.projects.models import Project
from core.decorators import login_required, require_permission
from core.views import  update_timeout
from app.stock.forms import UnitsForSizesForm
from app.stock.models import UnitsForSizes
from django.utils import simplejson

@login_required()
def overview(request):
    update_timeout(request)
    units = UnitsForSizes.objects.all()
    return render(request, 'stock/productUnits/list.html', {'title': 'Enheter', 'units': units})


@login_required()
def add(request):
    return form(request)


@login_required()
def edit(request, id):
    return form(request, id)


@login_required()
def delete(request, id):
    Project.objects.get(id=id).delete()
    return redirect(overview)


@require_permission("CREATE", UnitsForSizes)
def add_ajax(request):
    form = UnitsForSizesForm(request.POST, instance=UnitsForSizes())

    if form.is_valid():
        a = form.save()

        return HttpResponse(simplejson.dumps({'name': a.name,
                                              'valid': True,
                                              'id': a.id}), mimetype='application/json')


    else:
        errors = dict([(field, errors[0]) for field, errors in form.errors.items()])

        return HttpResponse(simplejson.dumps({'errors': errors,
                                              'valid': False}), mimetype='application/json')

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

    return render(request, "form.html", {'title': 'Enhet', 'form': form})
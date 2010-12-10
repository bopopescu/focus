# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from core.shortcuts import *
from core.decorators import *
from core.views import  updateTimeout
from app.stock.forms import UnitsForSizesForm
from app.stock.models import UnitsForSizes

@login_required()
def overview(request):
    updateTimeout(request)
    units = UnitsForSizes.objects.for_user()
    return render_with_request(request, 'stock/productUnits/list.html', {'title':'Enheter', 'units':units})

@login_required()
def add(request):
    return form(request)

def edit(request, id):
    return form(request, id)

def delete(request, id):
    Project.objects.get(id=id).delete()
    return redirect(overview)


@login_required()
def addPop(request):
    instance = UnitsForSizes()

    if request.method == "POST":
        form = UnitsForSizesForm(request.POST, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                            ((o._get_pk_val()), (o)))
    else:
        form = UnitsForSizesForm(instance=instance)

    return render_with_request(request, "simpleform.html", {'title':'Enhet', 'form': form })

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
            messages.success(request, msg)

            return redirect(overview)

    else:
        form = UnitsForSizesForm(instance=instance)

    return render_with_request(request, "form.html", {'title':'Enhet', 'form': form})
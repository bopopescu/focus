# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from forms import *
from core.shortcuts import *
from core.decorators import *
from core.views import updateTimeout

@login_required()
def overview(request):
    updateTimeout(request)
    suppliers = Supplier.objects.all()
    return render_with_request(request, 'suppliers/list.html', {'title': 'Leverandører', 'suppliers': suppliers})

@login_required()
def overview_deleted(request):
    suppliers = Supplier.objects.filter(deleted=True)
    return render_with_request(request, 'suppliers/list.html',
                               {'title': 'Slettede leverandører', 'suppliers': suppliers})

@login_required()
def overview_all(request):
    suppliers = Supplier.objects.all()
    return render_with_request(request, 'suppliers/list.html',
                               {'title': 'Alle aktive leverandører', 'suppliers': suppliers})

@login_required()
def add(request):
    return form(request)

def edit(request, id):
    return form(request, id)

@login_required()
def addPop(request):
    instance = Supplier()

    if request.method == "POST":
        form = SupplierForm(request.POST, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                    ((o._get_pk_val()), (o)))
    else:
        form = SupplierForm(instance=instance)

    return render_with_request(request, "simpleform.html", {'title': 'Kontakt', 'form': form})

def delete(request, id):
    Supplier.objects.get(id=id).delete()
    return redirect(overview)

@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(Supplier, id=id, deleted=False)
        msg = "Vellykket endret leverandør"
    else:
        instance = Supplier()
        msg = "Vellykket lagt til ny leverandør"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            request.message_success(msg)
            return redirect(overview)
    else:
        form = SupplierForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Leverandør',
                                                      'form': form,
                                                      })
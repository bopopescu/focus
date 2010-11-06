# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from core.shortcuts import *
from core.decorators import *
from core.views import form_perm, updateTimeout
from app.stock.forms import ProductGroupForm
from app.stock.models import ProductGroup

@login_required
def overview(request):
    updateTimeout(request)
    productgroups = ProductGroup.objects.for_user()
    return render_with_request(request, 'productgroups/list.html', {'title':'Produktgrupper', 'productgroups':productgroups})

@login_required
def add(request):
    return form(request)

@require_perm('change', ProductGroup)
def edit(request, id):
    return form(request, id)

@require_perm('delete', ProductGroup)
def delete(request, id):
    ProductGroup.objects.get(id=id).delete()
    return redirect(overview)


@login_required
def addPop(request):
    instance = ProductGroup()

    if request.method == "POST":
        form = ProductGroupForm(request.POST, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                            ((o._get_pk_val()), (o)))
    else:
        form = ProductGroupForm(instance=instance)

    return render_with_request(request, "simpleform.html", {'title':'Produktgruppe', 'form': form })


@login_required
def form (request, id = False):

    if id:
        instance = get_object_or_404(ProductGroup, id = id, deleted=False)
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
            messages.success(request, msg)

            return redirect(overview)

    else:
        form = ProductGroupForm(instance=instance)

    return render_with_request(request, "form.html", {'title':'Produktgruppe', 'form': form })
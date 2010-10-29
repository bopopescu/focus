# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required, permission_required
from forms import *
from core.shortcuts import *
from core.decorators import *
from core.views import form_perm, updateTimeout

@login_required
def overview(request):
    updateTimeout(request)
    suppliers = Supplier.objects.for_user()
    return render_with_request(request, 'suppliers/list.html', {'title':'Leverandører', 'suppliers':suppliers})

@login_required
def overview_deleted(request):
    contacts = Supplier.objects.for_company(deleted=True)
    return render_with_request(request, 'suppliers/list.html', {'title':'Slettede leverandører', 'contacts':contacts})

@login_required
def overview_all(request):
    contacts = Supplier.objects.for_company()
    return render_with_request(request, 'suppliers/list.html', {'title':'Alle aktive leverandører', 'contacts':contacts})

@login_required
def add(request):
    return form(request)

@require_perm('change', Contact)
def edit(request, id):
    return form(request, id)

@login_required
def addPop(request):
    instance = Contact()

    if request.method == "POST":
        form = SupplierForm(request.POST, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                            ((o._get_pk_val()), (o)))
    else:
        form = SupplierForm(instance=instance)

    return render_with_request(request, "simpleform.html", {'title':'Kontakt', 'form': form })

@require_perm('delete', Contact)
def delete(request, id):
    Contact.objects.get(id=id).delete()
    return redirect(overview)

def permissions(request, id):
    type = Supplier
    url = "suppliers/edit/%s" % id
    message = "Vellykket endret tilgang for leverandøren: %s" % type.objects.get(pk=id)
    return form_perm(request, type, id, url, message)

@login_required
def form (request, id = False):

    if id:
        instance = get_object_or_404(Supplier, id = id, deleted=False)
        msg = "Velykket endret leverandør"
    else:
        instance = Supplier()
        msg = "Velykket lagt til ny leverandlr"

    #Save and set to active, require valid form
    if request.method == 'POST':

        form = SupplierForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            messages.success(request, msg)
            if not id:
                return redirect(permissions, o.id)
            return redirect(overview)
    else:
        form = SupplierForm(instance=instance)

    return render_with_request(request, "form.html", {  'title':'Kontakt',
                                                        'form': form,
                                                    })
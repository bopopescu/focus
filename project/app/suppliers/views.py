# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from app.customers.models import Customer
from core.models import Log
from django.contrib.contenttypes.models import ContentType
from forms import *
from core.shortcuts import *
from core.decorators import *
from django.utils import simplejson
from core.views import updateTimeout
from django.utils.translation import ugettext as _

@login_required()
def overview(request):
    updateTimeout(request)
    suppliers = Core.current_user().getPermittedObjects("VIEW", Supplier).filter(trashed=False)
    return render_with_request(request, 'suppliers/list.html', {'title': _("Suppliers"), 'suppliers': suppliers})

@login_required()
def overview_trashed(request):
    updateTimeout(request)
    suppliers = Core.current_user().getPermittedObjects("VIEW", Supplier).filter(trashed=True)
    return render_with_request(request, 'suppliers/list.html',
                               {'title': _("Deleted suppliers"), 'suppliers': suppliers})

@login_required()
def overview_all(request):
    suppliers = Supplier.objects.all()
    return render_with_request(request, 'suppliers/list.html',
                               {'title': _("All active suppliers"), 'suppliers': suppliers})


@require_permission("CREATE", Customer)
def add_ajax(request):
    form = SupplierSimpleForm(request.POST, instance=Supplier())

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
def view(request, id):
    supplier = Core.current_user().getPermittedObjects("VIEW", Supplier).get(id=id)

    return render_with_request(request, 'suppliers/view.html',
                               {'title': _("Supplier"),
                                'supplier': supplier})


@require_permission("EDIT", Supplier, "id")
def history(request, id):
    instance = get_object_or_404(Supplier, id=id, deleted=False)

    history = Log.objects.filter(content_type=ContentType.objects.get_for_model(instance.__class__),
                                 object_id=instance.id)

    return render_with_request(request, 'suppliers/log.html', {'title': _("Latest events"),
                                                               'supplier': instance,
                                                               'logs': history[::-1][0:150]})

@login_required()
def add(request):
    return form(request)

def edit(request, id):
    return form(request, id)

@require_permission("DELETE", Customer, "id")
def trash(request, id):
    instance = Supplier.objects.get(id=id)

    if request.method == "POST":
        if not instance.canBeDeleted()[0]:
            request.message_error("You can't delete this supplier because: ")
            for reason in instance.canBeDeleted()[1]:
                request.message_error(reason)
        else:
            request.message_success("Successfully deleted this supplier")
            instance.trash()
        return redirect(overview)
    else:
        return render_with_request(request, 'suppliers/trash.html', {'title': _("Confirm delete"),
                                                                     'supplier': instance,
                                                                     'canBeDeleted': instance.canBeDeleted()[0],
                                                                     'reasons': instance.canBeDeleted()[1],
                                                                     })

@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(Supplier, id=id, deleted=False)
        msg = _("Successfully edited supplier")
    else:
        instance = Supplier()
        msg = _("Successfully addded new supplier")

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            request.message_success(msg)

            return redirect(view, o.id)
    else:
        form = SupplierForm(instance=instance)

    return render_with_request(request, "suppliers/form.html", {'title': _("Supplier"),
                                                                'supplier': instance,
                                                                'form': form,
                                                                })
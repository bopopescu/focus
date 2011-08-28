# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from app.customers.models import Customer
from app.stock.models import Product
from app.suppliers.forms import SupplierSimpleForm, SupplierForm
from app.suppliers.models import Supplier
from core import Core
from core.decorators import login_required, require_permission
from core.models import Log
from django.contrib.contenttypes.models import ContentType
from django.utils import simplejson
from core.views import update_timeout
from django.utils.translation import ugettext as _

@login_required()
def overview(request):
    update_timeout(request)
    suppliers = Core.current_user().get_permitted_objects("VIEW", Supplier).filter(trashed=False)
    return render(request, 'suppliers/list.html', {'title': _("Suppliers"), 'suppliers': suppliers})


@login_required()
def overview_trashed(request):
    update_timeout(request)
    suppliers = Core.current_user().get_permitted_objects("VIEW", Supplier).filter(trashed=True)
    return render(request, 'suppliers/list.html',
            {'title': _("Deleted suppliers"), 'suppliers': suppliers})


@login_required()
def overview_all(request):
    suppliers = Supplier.objects.all()
    return render(request, 'suppliers/list.html',
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
    supplier = Core.current_user().get_permitted_objects("VIEW", Supplier).get(id=id)

    return render(request, 'suppliers/view.html',
            {'title': _("Supplier"),
             'supplier': supplier})


@login_required()
def products(request, id):
    supplier = Core.current_user().get_permitted_objects("VIEW", Supplier).get(id=id)
    products = Core.current_user().get_permitted_objects("VIEW", Product).filter(supplier=supplier)

    return render(request, 'suppliers/products.html', {'title': _("Products"),
                                                       'supplier': supplier,
                                                       'products': products})


@require_permission("EDIT", Supplier, "id")
def history(request, id):
    instance = get_object_or_404(Supplier, id=id, deleted=False)

    history = Log.objects.filter(content_type=ContentType.objects.get_for_model(instance.__class__),
                                 object_id=instance.id)

    return render(request, 'suppliers/log.html', {'title': _("Latest events"),
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
        if not instance.can_be_deleted()[0]:
            request.message_error("You can't delete this supplier because: ")
            for reason in instance.can_be_deleted()[1]:
                request.message_error(reason)
        else:
            request.message_success("Successfully deleted this supplier")
            instance.trash()

        return redirect(overview)
    else:
        return render(request, 'suppliers/trash.html', {'title': _("Confirm delete"),
                                                        'supplier': instance,
                                                        'can_be_deleted': instance.can_be_deleted()[0],
                                                        'reasons': instance.can_be_deleted()[1],
                                                        })


@require_permission("DELETE", Customer, "id")
def restore(request, id):
    instance = Supplier.objects.get(id=id)

    if request.method == "POST":
        request.message_success("Successfully restored this customer")
        instance.restore()
        return redirect(view, instance.id)
    else:
        return render(request, 'suppliers/restore.html', {'title': _("Confirm restore"),
                                                          'supplier': instance,
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

    return render(request, "suppliers/form.html", {'title': _("Supplier"),
                                                   'supplier': instance,
                                                   'form': form,
                                                   })
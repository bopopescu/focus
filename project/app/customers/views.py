from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from app.customers.forms import CustomerFormSimple, CustomerForm, ContactToCustomerForm
from app.customers.models import Customer
from core import Core
from core.decorators import require_permission, login_required
from core.models import Log
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from core.views import update_timeout
from django.utils import simplejson
from django.utils.translation import ugettext as _

@require_permission("LIST", Customer)
def overview(request):
    update_timeout(request)
    customers = Core.current_user().get_permitted_objects("VIEW", Customer).filter(trashed=False)

    return render(request, 'customers/list.html', {'title': _('Customers'),
                                                   'customers': customers})


@require_permission("LISTDELETED", Customer)
def overview_trashed(request):
    customers = Customer.all_objects.filter(trashed=True, company=Core.current_user().get_company())
    return render(request, 'customers/list.html', {'title': _('Deleted customers'),
                                                   'customers': customers})


@require_permission("LISTALL", Customer)
def overview_all(request):
    customers = Customer.objects.all()
    return render(request, 'customers/list.html', {'title': _("All active customers"),
                                                   'customers': customers})


@require_permission("VIEW", Customer, 'id')
def view(request, id):
    customer = Core.current_user().get_permitted_objects("VIEW", Customer).get(id=id)

    return render(request, 'customers/view.html', {'title': _('Customer: ') + customer.name,
                                                   'customer': customer})


@require_permission("CREATE", Customer)
def add_ajax(request, id=None):
    customer = Customer()

    if id:
        customer = Customer.objects.filter_current_company().get(id=id)

    form = CustomerFormSimple(request.POST, instance=customer)

    if form.is_valid():
        a = form.save()

        return HttpResponse(simplejson.dumps({'name': a.name,
                                              'id': a.id,
                                              'valid': True}), mimetype='application/json')
    else:
        errors = dict([(field, errors[0]) for field, errors in form.errors.items()])

        return HttpResponse(simplejson.dumps({'errors': errors,
                                              'valid': False}), mimetype='application/json')

    return HttpResponse("ERROR")


@require_permission("EDIT", Customer, "id")
def history(request, id):
    instance = get_object_or_404(Customer, id=id, deleted=False)

    history = Log.objects.filter(content_type=ContentType.objects.get_for_model(instance.__class__),
                                 object_id=instance.id)

    return render(request, 'customers/log.html', {'title': _("Latest events"),
                                                  'customer': instance,
                                                  'logs': history[::-1][0:150]})


@require_permission("VIEW", Customer, "id")
def list_contacts(request, id):
    if request.method == "POST":
        form = ContactToCustomerForm(request.POST)
    else:
        form = ContactToCustomerForm()

    customer = Core.current_user().get_permitted_objects("VIEW", Customer).get(id=id)
    return render(request, 'customers/contacts.html',
                  {'title': unicode(customer.name) + " " + _('contacts'),
                   'form': form,
                   'customer': customer})


@require_permission("CREATE", Customer)
def add(request):
    return form(request)


@require_permission("EDIT", Customer, "id")
def edit(request, id):
    return form(request, id)


@require_permission("DELETE", Customer, "id")
def trash(request, id):
    customer = Customer.objects.get(id=id)

    if request.method == "POST":
        if not customer.can_be_deleted()[0]:
            request.message_error("You can't delete this customer because: ")
            for reason in customer.can_be_deleted()[1]:
                request.message_error(reason)
        else:
            request.message_success("Successfully deleted this customer")
            customer.trash()
        return redirect(overview)
    else:
        return render(request, 'customers/trash.html', {'title': _("Confirm delete"),
                                                        'customer': customer,
                                                        'can_be_deleted': customer.can_be_deleted()[0],
                                                        'reasons': customer.can_be_deleted()[1],
                                                        })


@require_permission("DELETE", Customer, "id")
def restore(request, id):
    customer = Customer.objects.get(id=id)

    if request.method == "POST":
        request.message_success("Successfully restored this customer")
        customer.restore()
        return redirect(view, customer.id)
    else:
        return render(request, 'customers/restore.html', {'title': _("Confirm restore"),
                                                          'customer': customer,
                                                          })


@login_required()
def form (request, id=False):
    if id:
        instance = Customer.objects.all().get(id=id)
        msg = _("Successfully edited customer")
        title = _("Edit customer")
        cid = instance.cid
    else:
        instance = Customer()
        msg = _("Successfully added new customer")
        title = _("New custmer")
        cid = Customer.calculate_next_cid()

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            request.message_success(msg)

            return redirect(view, o.id)
    else:
        form = CustomerForm(instance=instance, initial={'cid':cid})

    return render(request, "customers/form.html", {'title': title, 'customer': instance, 'form': form})
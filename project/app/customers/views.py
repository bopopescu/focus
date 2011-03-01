from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.http import HttpResponse
from core.models import Log
from django.shortcuts import get_object_or_404
from forms import *
from core.shortcuts import *
from core.decorators import *
from core.views import updateTimeout
from django.utils import simplejson
from django.utils.translation import ugettext as _

@require_permission("LIST", Customer)
def overview(request):
    updateTimeout(request)
    customers = Core.current_user().getPermittedObjects("VIEW", Customer).filter(trashed=False)

    return render_with_request(request, 'customers/list.html', {'title': _('Customers'),
                                                                'customers': customers})

@require_permission("LISTDELETED", Customer)
def overview_trashed(request):
    customers = Customer.all_objects.filter(trashed=True, company=Core.current_user().get_company())
    return render_with_request(request, 'customers/list.html', {'title': _('Deleted customers'),
                                                                'customers': customers})

@require_permission("LISTALL", Customer)
def overview_all(request):
    customers = Customer.objects.all()
    return render_with_request(request, 'customers/list.html', {'title': _("All active customers"),
                                                                'customers': customers})

@require_permission("VIEW", Customer, 'id')
def view(request, id):
    customer = Core.current_user().getPermittedObjects("VIEW", Customer).get(id=id)
    return render_with_request(request, 'customers/view.html', {'title': _('Customer: ') + customer.full_name,
                                                                'customer': customer})

@require_permission("CREATE", Customer)
def add_ajax(request):
    form = CustomerFormSimple(request.POST, instance=Customer())

    if form.is_valid():
        a = form.save()

        return HttpResponse(simplejson.dumps({'name': a.full_name,
                                              'id': a.id,
                                              'valid': True}), mimetype='application/json')
    else:
        errors = dict([(field, [unicode(error) for error in errors]) for field, errors in form.errors.items()])

        return HttpResponse(simplejson.dumps({'errors': '%s' % errors,
                                              'valid': False}), mimetype='application/json')

    return HttpResponse("ERROR")

@require_permission("EDIT", Customer, "id")
def history(request, id):
    instance = get_object_or_404(Customer, id=id, deleted=False)

    history = Log.objects.filter(content_type=ContentType.objects.get_for_model(instance.__class__),
                                 object_id=instance.id)

    return render_with_request(request, 'customers/log.html', {'title': _("Latest events"),
                                                               'customer': instance,
                                                               'logs': history[::-1][0:150]})

@require_permission("VIEW", Customer, "id")
def list_contacts(request, id):
    if request.method == "POST":
        form = ContactToCustomerForm(request.POST)
        print form
    else:
        form = ContactToCustomerForm()

    customer = Core.current_user().getPermittedObjects("VIEW", Customer).get(id=id)
    return render_with_request(request, 'customers/contacts.html',
                               {'title': unicode(customer.full_name) + " " + _('contacts'),
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
        if not customer.canBeDeleted()[0]:
            request.message_error("You can't delete this customer because: ")
            for reason in customer.canBeDeleted()[1]:
                request.message_error(reason)
        else:
            request.message_success("Successfully deleted this customer")
            customer.trash()
        return redirect(overview)
    else:
        return render_with_request(request, 'customers/trash.html', {'title': _("Confirm delete"),
                                                                     'customer': customer,
                                                                     'canBeDeleted': customer.canBeDeleted()[0],
                                                                     'reasons': customer.canBeDeleted()[1],
                                                                     })

@require_permission("DELETE", Customer, "id")
def recover(request, id):
    c = Customer.objects.get(id=id)
    c.recover()

    print c
    return redirect(overview)

@login_required()
def form (request, id=False):
    if id:
        instance = Customer.objects.all().get(id=id)
        msg = _("Successfully edited customer")
        title = _("Edit customer")
    else:
        instance = Customer()
        msg = _("Successfully added new customer")
        title = _("New custmer")

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
        form = CustomerForm(instance=instance)

    return render_with_request(request, "customers/form.html", {'title': title, 'customer': instance, 'form': form})
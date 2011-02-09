from django.core.mail import send_mail
from django.http import HttpResponse
from forms import *
from core.shortcuts import *
from core.decorators import *
from core.views import updateTimeout
from django.utils import simplejson

@require_permission("LIST", Customer)
def overview(request):
    updateTimeout(request)
    customers = Core.current_user().getPermittedObjects("VIEW", Customer).filter(trashed=False)

    return render_with_request(request, 'customers/list.html', {'title': 'Kunder',
                                                                'customers': customers})

@require_permission("LISTDELETED", Customer)
def overview_trashed(request):
    customers = Customer.all_objects.filter(trashed=True, company=Core.current_user().get_company())
    return render_with_request(request, 'customers/list.html', {'title': 'Slettede kunder',
                                                                'customers': customers})

@require_permission("LISTALL", Customer)
def overview_all(request):
    customers = Customer.objects.all()
    return render_with_request(request, 'customers/list.html', {'title': 'Alle aktive kunder',
                                                                'customers': customers})

@require_permission("VIEW", Customer, 'id')
def view(request, id):
    customer = Core.current_user().getPermittedObjects("VIEW", Customer).get(id=id)
    return render_with_request(request, 'customers/view.html', {'title': 'Kunde: %s' % customer.full_name,
                                                                'customer': customer})

@require_permission("CREATE", Customer)
def add_ajax(request):
    form = CustomerFormSimple(request.POST, instance=Customer())

    if form.is_valid():
        a = form.save()

        return HttpResponse(simplejson.dumps({'name': a.full_name,
                                              'id': a.id}), mimetype='application/json')

    return HttpResponse("ERROR")

@require_permission("CREATE", Customer)
def add(request):
    return form(request)


@require_permission("EDIT", Customer, "id")
def edit(request, id):
    return form(request, id)

@require_permission("DELETE", Customer, "id")
def trash(request, id):
    customer = Customer.objects.get(id=id)

    if not customer.canBeDeleted()[0]:
        request.message_error(customer.canBeDeleted()[1])
    else:
        customer.trash()

    return redirect(overview)

@require_permission("DELETE", Customer, "id")
def recover(request, id):
    c = Customer.objects.get(id=id)
    c.deleted = not c.deleted
    c.save()

    return redirect(overview)

@login_required()
def form (request, id=False):
    if id:
        instance = Customer.objects.all().get(id=id)
        msg = "Vellykket endret kunde"
        title = "Endre kunde"
    else:
        instance = Customer()
        msg = "Vellykket lagt til ny kunde"
        title = "Ny kunde"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            request.message_success(msg)

            return redirect(edit, o.id)
    else:
        form = CustomerForm(instance=instance)

    customers = Core.current_user().getPermittedObjects("VIEW", Customer)

    return render_with_request(request, "customers/form.html", {'title': title, 'customers': customers, 'form': form})
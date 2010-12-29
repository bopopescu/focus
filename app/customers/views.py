from forms import *
from core.shortcuts import *
from core.decorators import *
from core.views import form_perm, updateTimeout

@login_required()
def overview(request):
    updateTimeout(request)
    customers = Customer.objects.for_user()

    return render_with_request(request, 'customers/list.html', {'title': 'Kunder',
                                                                'customers': customers})

def overview_deleted(request):
    customers = Customer.objects.for_company(deleted=True)
    return render_with_request(request, 'customers/list.html', {'title': 'Slettede kunder',
                                                                'customers': customers})

def overview_all(request):
    customers = Customer.objects.for_company()
    return render_with_request(request, 'customers/list.html', {'title': 'Alle aktive kunder',
                                                                'customers': customers})

def view(request, id):
    customer = Customer.objects.for_user(deleted=None).get(id=id)
    return render_with_request(request, 'customers/view.html', {'title': 'Kunde: %s' % customer.full_name,
                                                                'customer': customer})


def addPop(request):
    instance = Customer()

    if request.method == "POST":
        form = CustomerFormSimple(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()

            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                    ((o._get_pk_val()), (o)))

    else:
        form = CustomerFormSimple(instance=instance)

    return render_with_request(request, "simpleform.html", {'title': 'Kunde', 'form': form})

def add(request):
    return form(request)

def edit(request, id):
    return form(request, id)

def delete(request, id):
    Customer.objects.get(id=id).delete()
    return redirect(overview)

def recover(request, id):
    c = Customer.objects.get(id=id)
    c.deleted = not c.deleted
    c.save()

    return redirect(overview)

def permissions(request, id, popup=False):
    type = Customer
    url = "customers/edit/%s" % id
    message = "Vellykket endret tilgang for kunde: %s" % type.objects.get(pk=id)
    return form_perm(request, type, id, url, message, popup)

def form (request, id=False):
    if id:
        instance = Customer.objects.for_user(deleted=None).get(id=id)
        msg = "Velykket endret kunde"
    else:
        instance = Customer()
        msg = "Velykket lagt til ny kunde"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=instance)
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
        form = CustomerForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Kunde', 'form': form})
from django.http import HttpResponse
from forms import *
from core.shortcuts import *
from core.decorators import *
from core.views import updateTimeout

@require_permission("LIST", Customer)
def overview(request):
    updateTimeout(request)
    customers = Customer.objects.all()

    return render_with_request(request, 'customers/list.html', {'title': 'Kunder',
                                                                'customers': customers})
@login_required()
def overview_deleted(request):
    customers = Customer.objects.filter(deleted=True)
    return render_with_request(request, 'customers/list.html', {'title': 'Slettede kunder',
                                                                'customers': customers})

@login_required()
def overview_all(request):
    customers = Customer.objects.all()
    return render_with_request(request, 'customers/list.html', {'title': 'Alle aktive kunder',
                                                                'customers': customers})

@login_required()
def view(request, id):
    customer = Customer.objects.filter(deleted=None).get(id=id)
    return render_with_request(request, 'customers/view.html', {'title': 'Kunde: %s' % customer.full_name,
                                                                'customer': customer})

@login_required()
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

@require_permission("CREATE", Customer)
def add(request):
    return form(request)

@login_required()
def edit(request, id):
    return form(request, id)

@login_required()
def delete(request, id):
    Customer.objects.get(id=id).delete()
    return redirect(overview)

@login_required()
def recover(request, id):
    c = Customer.objects.get(id=id)
    c.deleted = not c.deleted
    c.save()

    return redirect(overview)

@login_required()
def form (request, id=False):
    if id:
        instance = Customer.objects.all().get(id=id)
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
            request.message_success(msg)

            return redirect(overview)
    else:
        form = CustomerForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Kunde', 'form': form})
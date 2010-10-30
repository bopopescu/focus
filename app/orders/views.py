# -*- coding: utf-8 -*-

from forms import *
from core.shortcuts import *
from core.views import updateTimeout, form_perm
from core.decorators import *

@login_required
def overviewOffers(request):
    orders = Order.objects.for_user().filter(state="T")
    updateTimeout(request)
    return render_with_request(request, 'orders/list.html', {'title':'Ordrer', 'orders':orders})

@login_required
def overview(request):
    orders = Order.objects.for_user().filter(state="O")
    updateTimeout(request)
    return render_with_request(request, 'orders/list.html', {'title':'Ordrer', 'orders':orders})

@login_required
def overviewReadyForInvoice(request):
    orders = Order.objects.for_user().filter(state="F")
    updateTimeout(request)
    return render_with_request(request, 'orders/list.html', {'title':'Ordrer', 'orders':orders})

@login_required
def overviewArchive(request):
    orders = Order.objects.for_user().filter(state="A")
    updateTimeout(request)
    return render_with_request(request, 'orders/list.html', {'title':'Ordrer', 'orders':orders})


@require_perm('view', Order)
def view(request, id):
    order = Order.objects.for_company().get(id=id)
    whoCanSeeThis = order.whoHasPermissionTo('view')
    return render_with_request(request, 'orders/view.html', {'title':'Ordre: %s' % order.order_name,
                                                             'order':order,
                                                             'whoCanSeeThis':whoCanSeeThis})


@login_required
def changeStatus(request, orderID):


    order = Order.objects.get(id=orderID)

    if order.state == "T":
        order.state = "O"
    elif order.state == "O":
        order.state = "F"
    elif order.state == "F":
        order.state = "A"
    else:
        messages.error(request, "Ordren er arkivert og kan ikke forandres.")
        return redirect(overview)

    order.save()

    return redirect(view, order.id)

@login_required
def addOffer(request):
    return form(request, offer=True)

@login_required
def add(request):
    return form(request)

@login_required
def edit(request, id):
    return form(request, id)

@login_required
def delete(request, id):
    return form(request, id)


@login_required
def permissions(request, id):
    type = Order
    url = "orders/edit/%s" % id
    message = "Vellykket endret tilgang for ordre: %s" % type.objects.get(pk=id)
    return form_perm(request, type, id, url, message)


@login_required
def addPop(request):
    instance = Order()

    if request.method == "POST":
        form = OrderFormSimple(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()

            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                    ((o._get_pk_val()), (o)))
    else:
        form = OrderFormSimple(instance=instance)

    return render_with_request(request, "simpleform.html", {'title':'Ordre', 'form': form})

@login_required
def form (request, id=False, *args, **kwargs):

    title = "Ordre"
    if 'offer' in kwargs:
        title = "Tilbud"

    if id:
        instance = get_object_or_404(Order, id=id, deleted=False)
        msg = "Velykket endret ordre"

        #Sets title in template
        if instance.state == "T":
            title = "Tilbud"

    else:
        instance = Order()
        msg = "Velykket lagt til nytt ordre"


    #checks if order is to invoice og archived, if so, no edit is allowed
    if instance.state == "F":
        messages.error(request, "Ordren er til fakturering og kan ikke endres.")
        return redirect(overview)
    if instance.state == "A":
        messages.error(request, "Ordren er arkivert og kan ikke endres")
        return redirect(overview)


    #Save and set to active, require valid form
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)

            if not o.id:
                if 'offer' in kwargs:
                    o.state = "T"
                else:
                    o.state = "O"

            o.owner = request.user
            o.save()
            form.save_m2m()
            messages.success(request, msg)
            if not id:
                return redirect(permissions, o.id)
            return redirect(overview)

    else:
        form = OrderForm(instance=instance)

    return render_with_request(request, "form.html", {'title':title, 'form': form})

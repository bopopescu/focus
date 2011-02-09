# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from forms import *
from core.shortcuts import *
from core.views import updateTimeout
from core.decorators import *
from django.utils import simplejson

@require_permission("LIST", Order)
def overviewOffers(request):
    orders = Core.current_user().getPermittedObjects("VIEW", Order).filter(state="Offer")
    updateTimeout(request)
    return render_with_request(request, 'orders/list.html', {'title': 'Tilbud', 'orders': orders})

@require_permission("LIST", Order)
def overview(request):
    orders = Order.objects.all().filter(state="Order")
    updateTimeout(request)
    return render_with_request(request, 'orders/list.html', {'title': 'Ordrer', 'orders': orders})

@require_permission("LISTARCHIVE", Order)
def overviewReadyForInvoice(request):
    orders = Order.objects.all().filter(state="Invoice")
    updateTimeout(request)
    return render_with_request(request, 'orders/list.html', {'title': 'Til fakturering', 'orders': orders})

@require_permission("LISTREADYINVOICE", Order)
def overviewArchive(request):
    orders = Order.objects.all().filter(state="Archive")
    updateTimeout(request)
    return render_with_request(request, 'orders/list.html', {'title': 'Arkiv', 'orders': orders})


@require_permission("VIEW", Order, "id")
def view(request, id):
    order = Order.objects.all().get(id=id)
    whoCanSeeThis = order.whoHasPermissionTo('view')

    taskForm = TaskForm()

    return render_with_request(request, 'orders/view.html', {'title': 'Ordre: %s' % order.order_name,
                                                             'order': order,
                                                             'taskForm': taskForm,
                                                             'whoCanSeeThis': whoCanSeeThis})

@require_permission("VIEW", Order, "id")
def addTask(request, id):
    if request.method == "POST":
        order = Order.objects.all().get(id=id)
        form = TaskForm(request.POST, instance=Task())
        if form.is_valid():
            o = form.save(commit=False)
            o.order = order
            o.save()
            form.save_m2m()
        else:
            request.message_error("Ugyldig format")
    else:
        request.message_error("Du må skrive noe i feltet")

    return redirect(view, id)

@login_required()
def changeStatusTask(request, id):
    try:
        task = Task.objects.all().get(id=id)
        task.done = not task.done
        task.save()
    except:
        return redirect(overview)

    return redirect(view, task.order.id)

@require_permission("EDIT", Order, "id")
def changeStatus(request, id):
    order = Order.objects.get(id=id)

    if order.is_offer():
        pass
        #order.state = "O"
    elif order.is_order():
        pass
        #order.state = "F"
    elif order.is_ready_for_invoice():
        pass
        # order.state = "A"
    else:
        request.message_error("Ordren er arkivert og kan ikke forandres.")
        return redirect(overview)

    order.save()

    return redirect(view, order.id)

@require_permission("CREATE", Order)
def addOffer(request):
    return form(request, offer=True)

@require_permission("CREATE", Order)
def add(request):
    return form(request)

@require_permission("EDIT", Order, "id")
def edit(request, id):
    order = Order.objects.get(id=id)

    if not order.is_valid_for_edit():
        if order.is_archived():
            request.message_error("Ordren er arkivert og kan ikke forandres.")
        if order.is_ready_for_invoice():
            request.message_error("Ordren er klar til fakturering og kan ikke forandres.")
        return redirect(overview)

    return form(request, id)

@require_permission("DELETE", Order, "id")
def delete(request, id):
    order = Order.objects.get(id=id)

    if not order.is_valid_for_edit():
        if order.is_archived():
            request.message_error("Ordren er arkivert og kan ikke forandres.")
        if order.is_ready_for_invoice():
            request.message_error("Ordren er klar til fakturering og kan ikke forandres.")
        return redirect(overview)

    request.message_error("Det er ikke mulig å slette ordrer.")

    return view(request, id)

@login_required()
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

    return render_with_request(request, "simpleform.html", {'title': 'Ordre', 'form': form})

@login_required()
def form (request, id=False, *args, **kwargs):
    title = "Ordre"

    if 'offer' in kwargs:
        title = "Tilbud"

    if id:
        instance = get_object_or_404(Order, id=id, deleted=False)
        msg = "Velykket endret ordre"

        #Sets title in template
        if instance.is_offer():
            title = "Tilbud"

    else:
        instance = Order()
        msg = "Velykket lagt til nytt ordre"


    #checks if order is to invoice og archived, if so, no edit is allowed
    if instance.is_ready_for_invoice():
        request.message_error("Ordren er til fakturering og kan ikke endres.")
        return redirect(overview)

    if instance.is_archived():
        request.message_error("Ordren er arkivert og kan ikke endres")
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
            request.message_success(msg)

            return redirect(overview)

    else:
        form = OrderForm(instance=instance)

    return render_with_request(request, "form.html", {'title': title, 'form': form})

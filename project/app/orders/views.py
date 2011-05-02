# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from forms import *
from core.shortcuts import *
from core.views import update_timeout
from core.decorators import *
from django.utils import simplejson

@require_permission("LIST", Order)
def overview_offers(request):
    orders = Core.current_user().get_permitted_objects("VIEW", Order).filter(state="Offer")
    update_timeout(request)
    return render(request, 'orders/list.html', {'title': 'Tilbud', 'orders': orders})

@require_permission("LIST", Order)
def overview(request):
    orders = Core.current_user().get_permitted_objects("VIEW", Order).filter(state="Order")
    update_timeout(request)
    return render(request, 'orders/list.html', {'title': 'Ordrer', 'orders': orders})

@require_permission("LISTARCHIVE", Order)
def overview_invoice(request):
    orders = Order.objects.all().filter(state="Invoice")
    update_timeout(request)
    return render(request, 'orders/list.html', {'title': 'Til fakturering', 'orders': orders})

@require_permission("LISTREADYINVOICE", Order)
def overview_archive(request):
    orders = Order.objects.all().filter(state="Archive")
    update_timeout(request)

    return render(request, 'orders/list.html', {'title': 'Arkiv', 'orders': orders})

@require_permission("VIEW", Order, "id")
def products(request, id):
    order = Order.objects.get(id=id)
    order_lines = order.order_lines

    if request.method == "POST":
        form = OrderLineForm(request.POST, instance=OrderLine())
        o = form.save(commit=False)
        o.order = order
        o.save()
    else:
        form = OrderLineForm(instance=OrderLine())

    return render(request, 'orders/products.html', {'title': _('Products'),
                                                                 'form': form,
                                                                 'order': order,
                                                                 'order_lines': order_lines})

@require_permission("EDIT", Order, "id")
def delete_order_line(request, id, orderlineID):
    order = Order.objects.get(id=id)
    orderline = order.order_lines.get(id=orderlineID)
    orderline.delete()

    return redirect(products, id)

@require_permission("EDIT", Order, "id")
def history(request, id):
    instance = get_object_or_404(Order, id=id, deleted=False)
    history = instance.history()
    return render(request, 'orders/log.html', {'title': _("Latest events"),
                                                            'order': instance,
                                                            'logs': history[::-1][0:150]})

@require_permission("VIEW", Order, "id")
def view(request, id):
    order = Order.objects.all().get(id=id)
    who_can_see_this = order.who_has_permission_to('view')

    return render(request, 'orders/view.html', {'title': 'Ordre: %s' % order.order_name,
                                                             'order': order,
                                                             'who_can_see_this': who_can_see_this})

@require_permission("EDIT", Order, "id")
def change_status(request, id):
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
def add_offer(request):
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
        elif order.is_ready_for_invoice():
            request.message_error("Ordren er klar til fakturering og kan ikke forandres.")
        else:
            request.message_error("Du kan ikke endre denne ordren")

        return redirect(overview)

    offer = False
    if order.state == "Offer":
        offer = True

    return form(request, id, offer=True)

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

        if 'offer' in kwargs:
            form = OfferForm(request.POST, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)

            if not o.id:
                if 'offer' in kwargs:
                    o.state = "Offer"
                else:
                    o.state = "Order"

            o.save()
            form.save_m2m()
            request.message_success(msg)

            return redirect(view, o.id)

    else:
        form = OrderForm(instance=instance)
        if 'offer' in kwargs:
            form = OfferForm(instance=instance)

    return render(request, "orders/form.html", {'title': title, 'order': instance, 'form': form})

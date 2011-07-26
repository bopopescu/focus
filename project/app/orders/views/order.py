from django.shortcuts import render, get_object_or_404, redirect
from app.orders.forms import OrderForm, AddParticipantToOrderForm, CreateInvoiceForm
from app.orders.models import Order, ProductLine, Invoice
from app.stock.models import Product
from core import Core
from core.auth.log.models import Log
from core.auth.permission.models import Permission
from core.decorators import require_permission
from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from core.shortcuts import comment_block

@require_permission("LIST", Order)
def my_orders(request):
    orders = Core.current_user().get_permitted_objects("VIEW", Order).filter(trashed=False)
    return render(request, "orders/overview.html", {'title': 'Orders',
                                                    'orders': orders})


@require_permission("VIEW", Order)
def overview(request):
    orders = Order.objects.filter_current_company()
    return render(request, "orders/overview.html", {'title': 'Orders',
                                                    'orders': orders})


@require_permission("VIEW", Order)
def archive(request):
    orders = Order.archived_objects.filter_current_company()
    return render(request, "orders/overview.html", {'title': 'Orders',
                                                    'orders': orders})


@require_permission("VIEW", Order, "id")
def view_statistics(request, id):
    order = Order.objects.filter_current_company().get(id=id)
    return render(request, "orders/statistics.html", {'title': order.title,
                                                      'order': order})

@require_permission("EDIT", Order, "id")
def history(request, id):
    instance = get_object_or_404(Order, id=id, deleted=False)

    history = Log.objects.filter(content_type=ContentType.objects.get_for_model(instance.__class__),
                                 object_id=instance.id)

    return render(request, 'orders/log.html', {'title': _("Latest events"),
                                                  'order': instance,
                                                  'logs': history[::-1][0:150]})

@require_permission("VIEW", Order, "id")
def view(request, id):
    order = Order.objects.filter_current_company().get(id=id)
    comments = comment_block(request, order)
    who_can_see_this = order.who_has_permission_to('view')

    return render(request, "orders/view.html", {'title': order.title,
                                                'order': order,
                                                'comments': comments,
                                                'who_can_see_this':who_can_see_this})

def preview_order_html(request, id):
    order = Order.objects.filter_current_company().get(id=id)
    return render(request, "orders/pdf.html", {'order': order})


@require_permission("VIEW", Order, "id")
def create_invoice(request, id):
    order = Order.objects.filter_current_company().get(id=id)

    if request.method == "POST":

        form = CreateInvoiceForm(request.POST)

        if form.is_valid():
            #Create order based on offer
            invoice_number = request.POST['invoice_number']
            invoice = Invoice()
            invoice.invoice_number = int(invoice_number)
            invoice.order_id = order.id
            invoice.copy_from(order)

            #Archive the offer
            order.archived = True
            order.save()

            return redirect('app.invoices.views.view', invoice.id)

    else:
        form = CreateInvoiceForm()

    return render(request, "orders/create_invoice.html", {'title': order.title,
                                                          'order': order,
                                                          'next_invoice_number':Invoice.calculate_next_invoice_number(),
                                                          'form':form})


@require_permission("VIEW", Order)
def add(request):
    return form(request)


@require_permission("EDIT", Order, "id")
def edit(request, id):
    return form(request, id)


def form(request, id=None):
    products = []

    if id:
        instance = get_object_or_404(Order, id=id)
        products.extend(instance.product_lines.all())
        order_number = instance.order_number
    else:
        instance = Order()
        order_number = Order.calculate_next_order_number()

    if request.method == "POST":
        form = OrderForm(request.POST, instance=instance)
        products = []

        i = 0
        for p in request.POST.getlist('product_number'):
            p = ProductLine()
            p.description = request.POST.getlist('product_description')[i]
            p.price = request.POST.getlist('product_unit_cost')[i]
            p.count = request.POST.getlist('product_qty')[i]
            try:
                p.product = Product.objects.get(id=int(request.POST.getlist('product_number')[i]))
            except Exception, e:
                p.product = None

            products.append(p)
            i += 1

        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            o.update_products(products)

            request.message_success(_("Successfully saved order"))

            return redirect(view, o.id)
    else:
        form = OrderForm(instance=instance, initial={'order_number': order_number})

    return render(request, "orders/form.html", {'form': form,
                                                'order': instance,
                                                'products': products})

@require_permission("EDIT", Order, "id")
def delete_permission_from_participants(request, id, permission_id):
    permission = Permission.objects.get(id=permission_id)
    if not permission.user == Core.current_user():
        permission.delete()
        request.message_success("Deleted")
    else:
        request.message_error("You can't delete your own permissions")

    return participants(request, id, permission_id)

@require_permission("EDIT", Order, "id")
def participants(request, id, permission_id):

    order = get_object_or_404(Order, id=id)
    content_type = ContentType.objects.get_for_model(Order)

    if permission_id:
        permission = Permission.objects.get(id=permission_id)
    else:
        permission = Permission()

    if request.method == 'POST':
        form = AddParticipantToOrderForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['user']
            role = form.cleaned_data['role']

            perm = Permission()
            perm.content_type = content_type
            perm.object_id = id
            perm.user = user
            perm.role = role
            perm.save()

            request.message_success(_("Successfully add"))

    add_participant_to_group_form = AddParticipantToOrderForm()

    permissions = Permission.objects.filter(content_type=content_type, object_id=id)

    return render(request, "orders/participants.html", {'form': add_participant_to_group_form,
                                                        'order': order,
                                                        'permissions': permissions})
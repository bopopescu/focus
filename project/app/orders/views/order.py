from django.shortcuts import render, get_object_or_404, redirect
from app.orders.forms import OrderForm
from app.orders.models import Order, ProductLine, Invoice
from app.stock.models import Product
from core import Core
from core.decorators import require_permission
from django.utils.translation import ugettext as _

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
def view(request, id):
    order = Order.objects.filter_current_company().get(id=id)
    return render(request, "orders/view.html", {'title': order.title,
                                                'order': order})


def preview_order_html(request, id):
    order = Order.objects.filter_current_company().get(id=id)
    return render(request, "orders/pdf.html", {'order': order})


@require_permission("VIEW", Order, "id")
def create_invoice(request, id):
    order = Order.objects.filter_current_company().get(id=id)

    if request.method == "POST":
        #Create order based on offer
        invoice_number = request.POST['invoice_number']
        invoice = Invoice()
        invoice.invoice_number = int(invoice_number)
        invoice.order_id = order.id
        invoice.copy_from(order)
        invoice.save()

        #Archive the offer
        order.archived = True
        order.save()

        return redirect('app.invoices.views.view', invoice.id)

    return render(request, "orders/create_invoice.html", {'title': order.title,
                                                          'order': order})


def add(request):
    return form(request)


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
                product = Product.objects.get(id=int(request.POST.getlist('product_number')[i]))
                p.product = product
            except:
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

from django.shortcuts import render, get_object_or_404
from app.orders.models import Order
from core.decorators import require_permission

def overview(request):
    orders = Order.objects.all()
    return render(request, "order/overview.html", {'title':'Orders',
                                                  'orders':orders})

def archive(request):
    orders = Order.archived_objects.all()
    return render(request, "order/overview.html", {'title':'Orders',
                                                  'orders':orders})

@require_permission("VIEW", Order, "id")
def view(request, id):
    offer = Order.all_objects.get(id=id)
    return render(request, "offer/view.html", {'title': offer.title,
                                               'offer': offer})
from django.shortcuts import render, get_object_or_404
from app.orders.models import Order

def overview(request):
    return render(request, "order/overview.html")


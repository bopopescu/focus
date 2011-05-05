# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _
from app.client.models import ClientUser
from app.orders.forms import OfferForm
from app.orders.models import Order, Offer
from django.utils.translation import ugettext as _
from core.decorators import require_permission
from core.mail import send_mail
from django.conf import settings

def overview(request):
    offers = Offer.objects.all()
    return render(request, "offer/overview.html", {'title': _('Offers'),
                                                   'offers': offers})


@require_permission("VIEW", Offer, "id")
def view(request, id):
    offer = Offer.objects.get(id=id)
    return render(request, "offer/view.html", {'title': offer.title,
                                               'offer': offer})

def create_order(request, id):
    offer = Offer.objects.get(id=id)

    if request.method == "POST":
        #Create order based on offer
        order_number = request.POST['order_number']
        order = Order()
        order.copy_from(offer)
        order.order_number = int(order_number)
        order.save()

        #Archive the offer
        offer.archived = True
        offer.save()

        return redirect('app.orders.views.order.view', order.id)

    return render(request, "offer/create_order.html", {'title': offer.title,
                                                   'offer': offer})

def add(request):
    return form(request)


def client_management(request, id):
    offer = Offer.objects.get(id=id)

    if request.method == "POST":
        email_address = request.POST['email_address']
        client, created = ClientUser.objects.get_or_create(email=email_address)

        client.offers.add(offer)
        client.save()

        password_text = "Bruk din epostadresse og passord fra tidligere. Du kan også be om å få tilsendt nytt."
        if created:
            password = client.generate_password()
            client.set_password(password)
            client.save()
            password_text = "Bruk din epostadresse og passord: %s" % (password)

        message = """
        Hei. Du har fått tilsendt et nytt tilbud. Logg inn på %s for å se detaljer.

        %s

        """ % (settings.CLIENT_LOGIN_SITE, password_text)
        send_mail("Nytt tilbud", message, settings.NO_REPLY_EMAIL, [email_address])

    return render(request, "offer/client_management.html", {'offer': offer})


def edit(request, id):
    return form(request, id)

def form(request, id=None):
    if id:
        instance = get_object_or_404(Offer, id=id)
    else:
        instance = Offer()

    if request.method == "POST":
        form = OfferForm(request.POST, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            request.message_success(_("Successfully saved offer"))

            return redirect(view, o.id)
    else:
        form = OfferForm(instance=instance)

    return render(request, "offer/form.html", {'form': form, 'offer':instance})
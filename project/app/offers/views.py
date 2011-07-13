# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from app.client.models import ClientUser
from app.offers.forms import OfferForm
from app.orders.models import Order, Offer, ProductLine
from django.utils.translation import ugettext as _
from app.stock.models import Product
from core import Core
from core.auth.log.models import Log
from core.decorators import require_permission
from core.mail import send_mail
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

@require_permission("LIST", Offer)
def overview(request):
    offers = Core.current_user().get_permitted_objects("VIEW", Offer).filter(trashed=False)
    return render(request, "offers/overview.html", {'title': _('Offers'),
                                                    'offers': offers})

@require_permission("VIEW", Offer, "id")
def view(request, id):
    offer = Offer.objects.get(id=id)
    return render(request, "offers/view.html", {'title': offer.title,
                                                'offer': offer})

def create_order(request, id):
    offer = Offer.objects.get(id=id)

    if request.method == "POST":
        #Create order based on offer
        order_number = request.POST['order_number']
        order = Order()
        order.order_number = int(order_number)
        order.copy_from(offer)
        order.save()

        #Archive the offer
        offer.archived = True
        offer.save()

        return redirect('app.orders.views.order.view', order.id)

    return render(request, "offers/create_order.html", {'title': offer.title,
                                                        'offer': offer})


@require_permission("EDIT", Offer, "id")
def history(request, id):
    instance = get_object_or_404(Offer, id=id, deleted=False)

    history = Log.objects.filter(content_type=ContentType.objects.get_for_model(instance.__class__),
                                 object_id=instance.id)

    return render(request, 'offers/log.html', {'title': _("Latest events"),
                                                  'offer': instance,
                                                  'logs': history[::-1][0:150]})


@require_permission("ADD", Offer)
def add(request):
    return form(request)


@require_permission("EDIT", Offer, "id")
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

    return render(request, "offers/client_management.html", {'offer': offer})


@require_permission("EDIT", Offer, "id")
def edit(request, id):
    return form(request, id)


def form(request, id=None):
    products = []

    if id:
        instance = get_object_or_404(Offer, id=id)
        products.extend(instance.product_lines.all())
        offer_number = instance.offer_number
    else:
        instance = Offer()
        offer_number = Offer.calculate_next_offer_number()

    if request.method == "POST":
        form = OfferForm(request.POST, instance=instance)
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

            request.message_success(_("Successfully saved offer"))

            return redirect(view, o.id)
    else:
        form = OfferForm(instance=instance, initial={'offer_number': offer_number})

    return render(request, "offers/form.html", {'form': form,
                                                'offer': instance,
                                                'products': products})
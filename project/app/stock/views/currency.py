# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from app.projects.models import Project
from core.shortcuts import *
from core.decorators import *
from core.views import  updateTimeout
from app.stock.models import Currency
from django.utils import simplejson
from django.utils.translation import ugettext as _


@login_required()
def overview(request):
    updateTimeout(request)
    currencies = Currency.objects.all()
    return render_with_request(request, 'stock/currencies/list.html', {'title': 'Produkter', 'currencies': currencies})

@login_required()
def add(request):
    return form(request)

def edit(request, id):
    return form(request, id)

def delete(request, id):
    Project.objects.get(id=id).delete()
    return redirect(overview)

@require_permission("CREATE", Currency)
def add_ajax(request):
    form = CurrencyForm(request.POST, instance=Currency())

    if form.is_valid():
        a = form.save()

        return HttpResponse(simplejson.dumps({'name': a.name,
                                              'valid':True,
                                              'id': a.id}), mimetype='application/json')

    else:
        errors = dict([(field, errors[0]) for field, errors in form.errors.items()])

        return HttpResponse(simplejson.dumps({'errors': errors,
                                              'valid': False}), mimetype='application/json')

        return HttpResponse("ERROR")

@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(Currency, id=id, deleted=False)
        msg = "Velykket endret valuta"
    else:
        instance = Currency()
        msg = "Velykket lagt til nytt valuta"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = CurrencyForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            request.message_success(msg)

            return redirect(overview)

    else:
        form = CurrencyForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Valuta', 'form': form})


from app.stock.forms import CurrencyForm
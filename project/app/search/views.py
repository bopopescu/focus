from app.customers.models import Customer
from app.projects.models import Project
from app.contacts.models import Contact
from django.core.cache import cache
from app.tickets.models import Ticket, TicketUpdate
from core import Core
from core.decorators import login_required
from django.shortcuts import render
from app.orders.models import Order
from app.suppliers.models import Supplier
from app.stock.models import Product
from app.announcements.models import Announcement

@login_required()
def search(request):
    term = request.GET.get('s')

    cache_key = "%s_%s" % (Core.current_user().get_company().id, term)

    if cache.get(cache_key):
        return render(request, 'search/list.html', {'title': 'Resultat',
                                                    'objects': cache.get(cache_key)})

    searchIn = {}

    searchIn[Customer] = ["name", 'email', 'address', 'phone']
    searchIn[Project] = ["project_name", 'pid', 'responsible__first_name']
    searchIn[Contact] = ["name", "email", 'address', 'phone']
    searchIn[Ticket] = ["title", "description"]
    searchIn[TicketUpdate] = ["comment"]
    searchIn[Order] = ["title", "customer__name", 'project__project_name', 'description']
    searchIn[Supplier] = ["name"]
    searchIn[Product] = ['name', 'description', 'productGroup__name']
    searchIn[Announcement] = ["title", "text"]

    result = {}

    terms = term.split(" ")

    for o in searchIn.keys():
        for i in searchIn[o]:
            kwargs = {'%s__%s' % ('%s' % i, 'icontains'): '%s' % term}
            k = o.objects.filter_current_company().filter(**kwargs)

            for s in k:
                if s in result:
                    result[s] += 1
                else:
                    result[s] = 1

            for t in terms:
                kwargs = {'%s__%s' % ('%s' % i, 'icontains'): '%s' % t}
                k = o.objects.filter_current_company().filter(**kwargs)

                for s in k:
                    if s in result:
                        result[s] += 1
                    else:
                        result[s] = 1

    result = sorted(result.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

    v = []
    for i in result:
        v.append(i[0])

    cache.set(cache_key, v)

    return render(request, 'search/list.html', {'title': 'Resultat',
                                                'objects': v})
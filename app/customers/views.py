from django.core.mail import send_mail
from django.http import HttpResponse
from forms import *
from core.shortcuts import *
from core.decorators import *
from core.views import updateTimeout

@require_permission("LIST", Customer)
def overview(request):
    updateTimeout(request)
    customers = Core.current_user().getPermittedObjects("VIEW", Customer)

    print  Core.current_user().get_new_notifications()
    k = render_to_string('mail/dailyNotifications.html', {'companyName': 'Firma',
                                                          'notifications': Core.current_user().get_new_notifications()
                                                          })

    from django.core.mail import EmailMultiAlternatives

    subject, from_email, to = 'hello', 'frecarlsen@gmail.com', 'fredrik@fncit.no'
    text_content = 'This is an important message.'
    html_content = k
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return render_with_request(request, 'customers/list.html', {'title': 'Kunder',
                                                                'customers': customers})

@require_permission("LISTDELETED", Customer)
def overview_deleted(request):
    customers = Customer.objects.filter(deleted=True)
    return render_with_request(request, 'customers/list.html', {'title': 'Slettede kunder',
                                                                'customers': customers})

@require_permission("LISTALL", Customer)
def overview_all(request):
    customers = Customer.objects.all()
    return render_with_request(request, 'customers/list.html', {'title': 'Alle aktive kunder',
                                                                'customers': customers})

@require_permission("VIEW", Customer, 'id')
def view(request, id):
    customer = Core.current_user().getPermittedObjects("VIEW", Customer).get(id=id)
    return render_with_request(request, 'customers/view.html', {'title': 'Kunde: %s' % customer.full_name,
                                                                'customer': customer})

@login_required()
def addPop(request):
    instance = Customer()

    if request.method == "POST":
        form = CustomerFormSimple(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()

            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                    ((o._get_pk_val()), (o)))

    else:
        form = CustomerFormSimple(instance=instance)

    return render_with_request(request, "simpleform.html", {'title': 'Kunde', 'form': form})

@require_permission("CREATE", Customer)
def add(request):
    return form(request)

@require_permission("EDIT", Customer, "id")
def edit(request, id):
    return form(request, id)

@require_permission("DELETE", Customer, "id")
def delete(request, id):
    Customer.objects.get(id=id).delete()
    return redirect(overview)

@require_permission("DELETE", Customer, "id")
def recover(request, id):
    c = Customer.objects.get(id=id)
    c.deleted = not c.deleted
    c.save()

    return redirect(overview)

@login_required()
def form (request, id=False):
    if id:
        instance = Customer.objects.all().get(id=id)
        msg = "Velykket endret kunde"
    else:
        instance = Customer()
        msg = "Velykket lagt til ny kunde"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            request.message_success(msg)

            return redirect(overview)
    else:
        form = CustomerForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Kunde', 'form': form})
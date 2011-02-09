# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from forms import *
from core.shortcuts import *
from core.decorators import *
from core.views import updateTimeout

@login_required()
def overview(request):
    updateTimeout(request)
    contacts = Core.current_user().getPermittedObjects("VIEW", Contact).filter(trashed=False)
    return render_with_request(request, 'contacts/list.html', {'title': 'Kontakter', 'contacts': contacts})

@login_required()
def overview_trashed(request):
    contacts = Core.current_user().getPermittedObjects("VIEW", Contact).filter(trashed=True)
    return render_with_request(request, 'contacts/list.html', {'title': 'Slettede kontakter', 'contacts': contacts})

@login_required()
def overview_all(request):
    contacts = Core.current_user().getPermittedObjects("VIEW", Contact)
    return render_with_request(request, 'contacts/list.html', {'title': 'Alle aktive kontakter', 'contacts': contacts})

@require_permission("CREATE", Contact)
def add(request):
    return form(request)

@require_permission("EDIT", Contact, "id")
def edit(request, id):
    return form(request, id)

@require_permission("VIEW", Contact, "id")
def view(request, id):
    contact = get_object_or_404(Contact, id=id)
    return render_with_request(request, 'contacts/view.html', {'title': 'Kontakt', 'contact': contact})

@login_required()
def addPop(request):
    instance = Contact()

    if request.method == "POST":
        form = ContactForm(request.POST, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                    ((o._get_pk_val()), (o)))
    else:
        form = ContactForm(instance=instance)

    return render_with_request(request, "simpleform.html", {'title': 'Kontakt', 'form': form})

@require_permission("DELETE", Contact, "id")
def delete(request, id):
    Contact.objects.get(id=id).delete()
    return redirect(overview)

@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(Contact, id=id, deleted=False)
        msg = "Velykket endret kontakt"
    else:
        instance = Contact()
        msg = "Velykket lagt til ny kontakt"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            request.message_success(msg)

            return redirect(edit, o.id)
    else:
        form = ContactForm(instance=instance)

    contacts = Core.current_user().getPermittedObjects("VIEW", Contact)

    return render_with_request(request, "contacts/form.html", {'title': 'Kontakt',
                                                      'form': form,
                                                      'contacts':contacts,
                                                      })
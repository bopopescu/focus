# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from core.models import Log
from forms import *
from core.shortcuts import render_with_request, comment_block
from core.decorators import *
from core.views import updateTimeout
from django.utils import simplejson

@login_required()
def overview(request):
    updateTimeout(request)
    contacts = Core.current_user().getPermittedObjects("VIEW", Contact).filter(trashed=False)
    return render_with_request(request, 'contacts/list.html', {'title': _('Contacts'), 'contacts': contacts})

@login_required()
def overview_trashed(request):
    contacts = Core.current_user().getPermittedObjects("VIEW", Contact).filter(trashed=True)
    return render_with_request(request, 'contacts/list.html', {'title': _('Deleted contacts'), 'contacts': contacts})

@login_required()
def overview_all(request):
    contacts = Core.current_user().getPermittedObjects("VIEW", Contact)
    return render_with_request(request, 'contacts/list.html',
                               {'title': _("All deleted contacts"), 'contacts': contacts})

@require_permission("CREATE", Contact)
def add(request):
    return form(request)

@require_permission("EDIT", Contact, "id")
def history(request, id):
    contact = get_object_or_404(Contact, id=id, deleted=False)

    history = Log.objects.filter(content_type=ContentType.objects.get_for_model(contact.__class__),
                                 object_id = contact.id)
    
    return render_with_request(request, 'contacts/log.html', {'title': _("Latest events"),
                                                              'contact':contact,
                                                                            'logs': history[::-1][0:150]})

@require_permission("EDIT", Contact, "id")
def edit(request, id):
    return form(request, id)

@require_permission("VIEW", Contact, "id")
def view(request, id):
    contact = get_object_or_404(Contact, id=id)
    comments = comment_block(request, contact)
    return render_with_request(request, 'contacts/view.html', {'title': _('Contact'), 'comments':comments, 'contact': contact})

@require_permission("DELETE", Contact, "id")
def delete(request, id):
    Contact.objects.get(id=id).delete()
    return redirect(overview)

@require_permission("CREATE", Contact)
def add_ajax(request):
    form = ContactForm(request.POST, instance=Contact())

    if form.is_valid():
        a = form.save()

        return HttpResponse(simplejson.dumps({'name': a.full_name,
                                              'id': a.id}), mimetype='application/json')
    return HttpResponse("ERROR")


@require_permission("EDIT",Contact,"id")
def editImage(request, id):
    instance = get_object_or_404(Contact, id=id, deleted=False)
    msg = _("Successfully changed image")

    
    if request.method == 'POST':
        form = ContactImageForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            request.message_success(msg)

            return redirect(view, o.id)
    else:
        form = ContactImageForm(instance=instance, initial={"image":None})

    return render_with_request(request, "contacts/form.html", {'title': _("Contact"),
                                                               'form': form,
                                                               'contact': instance,
                                                               })

@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(Contact, id=id, deleted=False)
        msg = _("Successfully edited contact")
    else:
        instance = Contact()
        msg = _("Successfully added new contact")

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            request.message_success(msg)

            return redirect(edit, o.id)
    else:
        form = ContactForm(instance=instance)

    return render_with_request(request, "contacts/form.html", {'title': _("Contact"),
                                                               'form': form,
                                                               'contact': instance,
                                                               })
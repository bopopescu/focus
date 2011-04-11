# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from app.customers.models import Customer
from core.models import Log
from core.utils import suggest_ajax_parse_arguments
from forms import *
from core.shortcuts import comment_block
from core.decorators import *
from core.views import update_timeout
from django.utils import simplejson
from django.utils.simplejson import JSONEncoder

@login_required()
def overview(request):
    update_timeout(request)
    contacts = Core.current_user().get_permitted_objects("VIEW", Contact).filter(trashed=False)
    return render(request, 'contacts/list.html', {'title': _('Contacts'), 'contacts': contacts})


def list_ajax(request, query, limit):
    users = request.user.get_permitted_objects("LIST", Contact).filter(
        Q(username__startswith=query) |
        Q(surname__istartswith=query) |
        Q(name__istartswith=query) |
        Q(mail__istartswith=query)
    )[:limit]

    users = [{'id': user.id,
              'label': "%s (%s)" % (user.username, ("%s %s" % (user.name, user.surname)).strip()),
              'value': user.username} for user in users]
    return HttpResponse(JSONEncoder().encode(users), mimetype='application/json')


@login_required()
def overview_trashed(request):
    contacts = Core.current_user().get_permitted_objects("VIEW", Contact).filter(trashed=True)
    return render(request, 'contacts/list.html', {'title': _('Deleted contacts'), 'contacts': contacts})


@login_required()
def overview_all(request):
    contacts = Core.current_user().get_permitted_objects("VIEW", Contact)
    return render(request, 'contacts/list.html',
                               {'title': _("All deleted contacts"), 'contacts': contacts})


@require_permission("CREATE", Contact)
def add(request):
    return form(request)


@require_permission("EDIT", Contact, "id")
def history(request, id):
    contact = get_object_or_404(Contact, id=id, deleted=False)

    history = Log.objects.filter(content_type=ContentType.objects.get_for_model(contact.__class__),
                                 object_id=contact.id)

    return render(request, 'contacts/log.html', {'title': _("Latest events"),
                                                              'contact': contact,
                                                              'logs': history[::-1][0:150]})


@require_permission("EDIT", Contact, "id")
def edit(request, id):
    return form(request, id)


@require_permission("VIEW", Contact, "id")
def view(request, id):
    contact = get_object_or_404(Contact, id=id)
    comments = comment_block(request, contact)
    return render(request, 'contacts/view.html',
                               {'title': _('Contact'), 'comments': comments, 'contact': contact})


@require_permission("DELETE", Contact, "id")
def trash(request, id):
    instance = Contact.objects.get(id=id)

    if request.method == "POST":
        if not instance.can_be_deleted()[0]:
            request.message_error("You can't delete this contact because: ")
            for reason in instance.can_be_deleted()[1]:
                request.message_error(reason)
        else:
            request.message_success("Successfully contact this contact")
            instance.trash()
        return redirect(overview)
    else:
        return render(request, 'contacts/trash.html', {'title': _("Confirm delete"),
                                                                    'contact': instance,
                                                                    'can_be_deleted': instance.can_be_deleted()[0],
                                                                    'reasons': instance.can_be_deleted()[1],
                                                                    })


@suggest_ajax_parse_arguments()
def autocomplete(request, query, limit):
    contacts = Contact.objects.filter_current_company().filter(
        Q(full_name__startswith=query)
    )[:limit]

    contacts = [{'id': contact.id,
                 'label': "%s" % (contact.full_name),
                 'value': contact.full_name} for contact in contacts]

    return HttpResponse(JSONEncoder().encode(contacts), mimetype='application/json')


@require_permission("CREATE", Contact)
def add_ajax(request):
    form = ContactForm(request.POST, instance=Contact())

    if form.is_valid():
        a = form.save()

        return HttpResponse(simplejson.dumps({'name': a.full_name,
                                              'valid': True,
                                              'id': a.id}), mimetype='application/json')

    else:
        errors = dict([(field, errors[0]) for field, errors in form.errors.items()])

        return HttpResponse(simplejson.dumps({'errors': errors,
                                              'valid': False}), mimetype='application/json')

    return HttpResponse("ERROR")


@require_permission("EDIT", Contact, "id")
def edit_image(request, id):
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
        form = ContactImageForm(instance=instance, initial={"image": None})

    return render(request, "contacts/form.html", {'title': _("Contact"),
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

            return redirect(view, o.id)
    else:
        form = ContactForm(instance=instance)

    return render(request, "contacts/form.html", {'title': _("Contact"),
                                                               'form': form,
                                                               'contact': instance,
                                                               })
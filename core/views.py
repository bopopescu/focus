# -*- coding: utf-8 -*-
from core.decorators import login_required

@login_required()
def updateTimeout(request):
    request.session.set_expiry(1800)
    return

"""
@login_required()
def form_perm(request, type, id, url, message, popup=False):
    object = type.objects.get(pk=id)
    content_type = ContentType.objects.get_for_model(type)

    url_array = str.rsplit(str(url), "/")
    error = False

    if request.method == 'POST':
        formset = PermFormSet(request.POST, prefix="users")
        if formset.is_valid():
            instances = formset.save(commit=False)
            for o in instances:
                o.content_type = content_type
                o.object_id = id

                if o.user is not None:
                #if not Permission.exists() or o.id is None:
                    o.save()
                    messages.success(request, message)

                else:
                    error = True

        formset = PermFormSet(request.POST, prefix="memberships")
        if formset.is_valid():
            instances = formset.save(commit=False)
            for o in instances:
                o.content_type = content_type
                o.object_id = id

                if o.membership is not None:
                #if not Permission.exists() or o.id is None:
                    o.save()
                    messages.success(request, message)

                else:
                    error = True

        ObjectPermission.objects.filter(user=None, membership=None).delete()
        ObjectPermission.objects.filter(deleted=True).delete()

        if error:
            messages.error(request, "Kun gyldige kombinasjoner ble lagret")
            return HttpResponseRedirect("/%s/permissions/%s" % (url_array[0], url_array[2]))

        if popup:
            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                    ((o._get_pk_val()), (o)))

        return HttpResponseRedirect("/%s" % (url))

    else:
        if ObjectPermission.objects.filter(content_type=content_type,
                                           object_id=id).count() == 0 and object.creator == request.user:
            k = ObjectPermission(content_type=content_type, object_id=id, user=request.user, can_view=True,
                                 can_change=True, can_delete=True)
            k.save()

        PermSet = PermFormSet(
                queryset=ObjectPermission.objects.filter(content_type=content_type, object_id=id, membership=None),
                prefix="users")
        PermGroupSet = PermFormSet(
                queryset=ObjectPermission.objects.filter(content_type=content_type, object_id=id, user=None),
                prefix="memberships")

        if popup:
            return render_with_request(request, "form_perm_simple.html",
                                       {'title': 'Tildel rettigheter for: %s' % (object), 'form_perm': PermSet,
                                        'PermGroupSet': PermGroupSet})

        return render_with_request(request, "form_perm.html",
                                   {'title': 'Tildel rettigheter for: %s' % (object), 'form_perm': PermSet,
                                    'PermGroupSet': PermGroupSet})

"""
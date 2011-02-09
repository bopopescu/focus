# -*- coding: utf-8 -*-
import mimetypes
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from core.decorators import login_required
from core.models import User, Group
from django.core import urlresolvers
from django.shortcuts import redirect
import os
import django.contrib.auth.decorators as auth_decorators
import django.http
from django.core.servers.basehttp import FileWrapper
from settings import BASE_PATH

STATIC_ROOT = os.path.join(BASE_PATH,"uploads")

def get_absolute_filename(filename='', safe=True):
    if not filename:
        return os.path.join(STATIC_ROOT, 'index')
    if safe and '..' in filename.split(os.path.sep):
        return get_absolute_filename(filename='')
    
    return os.path.join(STATIC_ROOT, filename)

def retrieve_file(request, filename=''):
    abs_filename = get_absolute_filename(filename)


    mimetypes.add_type('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx', True)
    mime = mimetypes.guess_type(abs_filename)

    wrapper = FileWrapper(file(abs_filename))
    response = HttpResponse(wrapper, content_type=mime[0])
    response['Content-Length'] = os.path.getsize(abs_filename)
    return response


@login_required()
def updateTimeout(request):
    request.session.set_expiry(1800)
    return


def testing(request):
    return HttpResponse("OK")

"""

For granting permission on-site

Use like this: /grant/role/Admin/user/user_id/customers/customer/customer_id/

"""

def grant_role(request, role, userorgroup, user_id, app, model, object_id):
    object_type = ContentType.objects.get(app_label=app, model=model)

    if userorgroup.upper() == 'USER':
        obj = User.objects.get(id=user_id)
    elif userorgroup.upper() == 'GROUP':
        obj = Group.objects.get(id=user_id)
    else:
        request.message_error("An error occoured")
        return redirect(urlresolvers.reverse('app.dashboard.views.overview'))

    if object_id == "any":
        obj.grant_role(role, object_type.model_class())
    else:
        object = object_type.get_object_for_this_type(id=object_id)
        obj.grant_role(role, object)

    request.message_success("Role granted")
    return redirect(urlresolvers.reverse('app.dashboard.views.overview'))

"""

For granting permission on-site

Use like this: /grant/permission/ADD/user/user_id/customers/customer/customer_id/

"""

def grant_permission(request, perm, userorgroup, user_id, app, model, object_id):
    object_type = ContentType.objects.get(app_label=app, model=model)
    list = []
    list.append(perm.upper())

    if userorgroup.upper() == 'USER':
        obj = User.objects.get(id=user_id)
    elif userorgroup.upper() == 'GROUP':
        obj = Group.objects.get(id=user_id)
    else:
        request.message_error("An error occoured")
        return redirect(urlresolvers.reverse('app.dashboard.views.overview'))

    if object_id == "any":
        obj.grant_permissions(list, object_type.model_class())
    else:
        object = object_type.get_object_for_this_type(id=object_id)
        obj.grant_permissions(list, object)

    request.message_success("Permission granted")
    return redirect(urlresolvers.reverse('app.dashboard.views.overview'))


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
# -*- coding: utf-8 -*-
import mimetypes
import os
import urllib
import json
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from core.decorators import login_required
from django.core import urlresolvers
from django.shortcuts import redirect
from django.core.servers.basehttp import FileWrapper
from settings import BASE_PATH
from core.auth.user.models import User
from core.auth.group.models import Group
from django.utils.translation import ugettext as _
from django.utils import simplejson

STATIC_ROOT = os.path.join(BASE_PATH, "uploads")

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

def view_postal_by_zip(request, zip):
    if request.is_ajax():
            return HttpResponse(simplejson.dumps({'zip':zip, 'postal': str(get_postal_by_zip(zip)),}), mimetype='application/json')
    return HttpResponse(get_postal_by_zip(zip))
 
def get_postal_by_zip(zip):

    zip = zip.strip()

    if not len(zip):
        return ""
    
    if len(zip)<4:
           zip = (4-(len(zip)))*"0"+zip

    url = "http://fraktguide.bring.no/fraktguide/postalCode.json?pnr=" + zip + "&callback=?"
    f = urllib.urlopen(url)
    result = json.loads(f.read())

    if result['valid']:
        result= str(result['result']).capitalize()
    else:
        result = _("invalid zip")

    return result

@login_required()
def update_timeout(request):
    request.session.set_expiry(1800)
    return

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


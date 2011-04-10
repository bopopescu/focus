# -*- coding: utf-8 -*-
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from app.admin.forms import *
from core.decorators import login_required
from core.models import Group
from core.shortcuts import *
from core.views import updateTimeout
from django.utils.translation import ugettext as _

@login_required()
def overview(request):
    updateTimeout(request)

    groups = Core.current_user().getPermittedObjects("VIEW", Group)
    return render_with_request(request, 'admin/groups/list.html', {'title': _("Groups"), 'groups': groups})

def add(request):
    return form(request)

@login_required()
def edit(request, id):
    return form(request, id)

@login_required()
def addPop(request):
    instance = User()

    if request.method == "POST":
        form = GroupForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()

            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                    ((o._get_pk_val()), (o)))

    else:
        form = GroupForm(instance=instance)

    return render_with_request(request, "simpleform.html", {'title': 'Bruker', 'form': form})


@login_required()
def view(request, id):
    group = Group.objects.inCompany().get(id=id)
    return render_with_request(request, 'admin/groups/view.html', {'title': _("Groups"),
                                                                   'group': group,
                                                                   })
login_required()
def permissions(request, id):
    group = Core.current_user().getPermittedObjects("VIEW", Group).get(id=id)

    return render_with_request(request, 'admin/permissions.html', {'title': _("Groups"),
                                                                   'group': group,
                                                                   })



@login_required()
def delete(request, id):
    group = Core.current_user().getPermittedObjects("VIEW", Group).get(id=id)
    group.delete()

    request.message_success(_("Successfully deleted group"))
    return redirect(overview)

@login_required()
def form (request, id=False):
    if id:
        instance = Core.current_user().getPermittedObjects("VIEW", Group).get(id=id)
        msg = _("Successfully edited group")
    else:
        instance = Group()
        msg = _("Successfully added new group")

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.company = Core.current_user().get_company()
            o.save()
            form.save_m2m()

            request.message_success(msg)
            return redirect(overview)

    else:
        form = GroupForm(instance=instance)

    return render_with_request(request, "admin/groups/form.html",
                               {'title': _("Group"), 'group': instance, 'form': form})
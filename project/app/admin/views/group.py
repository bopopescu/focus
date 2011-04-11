# -*- coding: utf-8 -*-
from django.shortcuts import redirect, HttpResponse, render
from app.admin.forms import GroupForm
from core import Core
from core.auth.user.models import User
from core.decorators import login_required
from core.views import update_timeout
from django.utils.translation import ugettext as _
from core.auth.group.models import Group

@login_required()
def overview(request):
    update_timeout(request)

    groups = Core.current_user().get_permitted_objects("VIEW", Group)
    return render(request, 'admin/groups/list.html', {'title': _("Groups"), 'groups': groups})

def add(request):
    return form(request)

@login_required()
def edit(request, id):
    return form(request, id)

@login_required()
def view(request, id):
    group = Group.objects.filter_current_company().get(id=id)
    return render(request, 'admin/groups/view.html', {'title': _("Groups"),
                                                                   'group': group,
                                                                   })
login_required()
def permissions(request, id):
    group = Core.current_user().get_permitted_objects("VIEW", Group).get(id=id)

    return render(request, 'admin/permissions.html', {'title': _("Groups"),
                                                                   'group': group,
                                                                   })

@login_required()
def delete(request, id):
    group = Core.current_user().get_permitted_objects("VIEW", Group).get(id=id)
    group.delete()

    request.message_success(_("Successfully deleted group"))
    return redirect(overview)

@login_required()
def form (request, id=False):
    if id:
        instance = Core.current_user().get_permitted_objects("VIEW", Group).get(id=id)
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

    return render(request, "admin/groups/form.html",
                               {'title': _("Group"), 'group': instance, 'form': form})
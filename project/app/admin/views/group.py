# -*- coding: utf-8 -*-
from django.shortcuts import redirect, HttpResponse, render
from app.admin.forms import GroupForm, AddMemberToGroupForm, PermissionForm
from core import Core
from core.auth.permission.models import Permission
from core.auth.user.models import User
from core.decorators import login_required
from core.views import update_timeout
from django.utils.translation import ugettext as _
from core.auth.group.models import Group

@login_required()
def overview(request):
    update_timeout(request)

    groups = Group.objects.filter_current_company()
    return render(request, 'admin/groups/list.html', {'title': _("Groups"), 'groups': groups})


def add(request):
    return form(request)


@login_required()
def edit(request, id):
    return form(request, id)


@login_required()
def view(request, id):
    group = Group.objects.filter_current_company().get(id=id)
    return render(request, 'admin/groups/view.html', {'title': group.name,
                                                      'group': group,
                                                      })


@login_required()
def delete_permission(request, id, permission_id):
    group = Group.objects.get(id=id)
    perm = group.get_permissions().filter(id=permission_id)
    perm.delete()
    return redirect(permissions, id)


@login_required()
def permissions(request, id):
    group = Core.current_user().get_permitted_objects("VIEW", Group).get(id=id)

     #Save and set to active, require valid form
    if request.method == 'POST':
        permission_form = PermissionForm(request.POST, instance=Permission())
        if permission_form.is_valid():
            perm = permission_form.save(commit=False)
            perm.group = group
            perm.save()

    else:
        permission_form = PermissionForm(instance=Permission())

    return render(request, 'admin/permissions.html', {'title': _("Groups"),
                                                      'group': group,
                                                      'form': permission_form,                                                      
                                                      'permissions': group.get_permissions(),
                                                      })


@login_required()
def remove_user_from_group(request, group_id, user_id):
    user = User.objects.get(id=user_id)
    group = Group.objects.get(id=group_id)
    group.remove_member(user)

    return redirect(members, group_id)


@login_required()
def members(request, id):
    group = Core.current_user().get_permitted_objects("VIEW", Group).get(id=id)

    if request.method == 'POST':
        form = AddMemberToGroupForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['user']

            group.add_member(user)

    addMemberToGroupForm = AddMemberToGroupForm()
    addMemberToGroupForm.fields['user'].queryset = User.objects.filter_current_company()

    return render(request, 'admin/groups/members.html', {'title': _("Groups"),
                                                         'group': group,
                                                         'form': addMemberToGroupForm
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
# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import ugettext as _
from app.admin.forms import HourRegistrationManuallyForm, UserForm, PermissionForm
from core import Core
from core.decorators import login_required, require_permission
from core.views import update_timeout
from core.mail import send_mail
from core.auth.user.models import User
from core.auth.permission.models import Permission

@require_permission("MANAGE", User)
def overview(request):
    update_timeout(request)
    Users = User.objects.filter_current_company()
    return render(request, 'admin/users/list.html', {'title': _("Users"), 'users': Users})


@require_permission("CREATE", User)
def add(request):
    return form(request)


@require_permission("EDIT", User, "id")
def edit(request, id):
    return form(request, id)


@require_permission("EDIT", User, "id")
def editProfile(request):
    pass


@require_permission("EDIT", User, "id")
def changeCanLogin(request, id):
    u = User.objects.get(id=id)

    if u == request.user:
        request.messages_error(_("You can't change your own login status"))
        return redirect(view, id)

    u.canLogin = not u.canLogin
    u.save()
    return redirect(view, id)


def generate_new_password_for_user(user):
    import string
    import random

    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = [a for a in string.ascii_lowercase if a not in vowels]
    ret = ''
    slen = 8
    for i in range(slen):
        if i % 2 == 0:
            randid = random.randint(0, 20) #number of consonants
            ret += consonants[randid]
        else:
            randid = random.randint(0, 4) #number of vowels
            ret += vowels[randid]
    ret += "%s" % random.randint(20, 99)
    send_mail(_("New password"), (_("Your username is: %s" % user.username) + _("\nYour password is: ") + '%s' % ret),
              settings.NO_REPLY_EMAIL,
              [user.email], fail_silently=False)

    user.set_password("%s" % ret)
    
    user.save()
    return ret


@require_permission("EDIT", User, "id")
def send_generated_password_to_user(request, id):
    user = get_object_or_404(User, id=id, company=Core.current_user().get_company())
    generate_new_password_for_user(user)
    request.message_success(_("Successfully sent new password"))
    return redirect(view, id)


@require_permission("VIEW", User, "id")
def history(request, id):
    user = User.objects.get(id=id)
    history = user.logs.all()
    return render(request, 'admin/log.html', {'title': _("Latest events"),
                                              'userCard': user,
                                              'logs': history[::-1][0:150]})


@require_permission("VIEW", User, "id")
def view(request, id):
    user = User.objects.get(id=id)

    return render(request, 'admin/users/view.html', {'title': _("User"),
                                                     'userCard': user,
                                                     })


@require_permission("EDIT", User, "id")
def delete_permission(request, id, permission_id):
    user = User.objects.get(id=id)
    perm = user.get_permissions().filter(id=permission_id)
    perm.delete()
    return redirect(permissions, id)

@require_permission("EDIT", User, "id")
def permissions(request, id):
    user = User.objects.get(id=id)
    Permissions = user.get_permissions().order_by("group","content_type", "object_id")

    #Save and set to active, require valid form
    if request.method == 'POST':
        permission_form = PermissionForm(request.POST, instance=Permission())
        if permission_form.is_valid():
            perm = permission_form.save(commit=False)
            perm.user = user
            perm.save()
            
    else:
        permission_form = PermissionForm(instance=Permission())

    return render(request, 'admin/permissions.html', {'title': _("Permissions for %s" % user),
                                                      'userCard': user,
                                                      'form': permission_form,
                                                      'permissions': Permissions,
                                                      })

@require_permission("DELETE", User, "id")
def trash(request, id):
    instance = User.objects.get(id=id)

    if request.method == "POST":
        if not instance.can_be_deleted()[0]:
            request.message_error("You can't delete this user because: ")
            for reason in instance.can_be_deleted()[1]:
                request.message_error(reason)
        else:
            request.message_success("Successfully deleted this user")
            instance.trash()
        return redirect(overview)
    else:
        return render(request, 'admin/users/trash.html', {'title': _("Confirm delete"),
                                                          'userCard': instance,
                                                          'can_be_deleted': instance.can_be_deleted()[0],
                                                          'reasons': instance.can_be_deleted()[1],
                                                          })


@require_permission("EDIT", User, "id")
def set_hourregistration_limits (request, id):
    instance = get_object_or_404(User, id=id)
    msg = _("User successfully edited")

    if request.method == 'POST':
        form = HourRegistrationManuallyForm(request.POST, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)

            o.save()
            form.save_m2m()

            request.message_success(msg)

            return redirect(view, id)

    else:
        form = HourRegistrationManuallyForm(instance=instance)

    return render(request, "admin/users/form.html", {'title': _("Change user"),
                                                     'userCard': instance,
                                                     'form': form})


@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(User, id=id, company=request.user.company)
        msg = _("User successfully added")
    else:
        instance = User()
        msg = _("New user successfully added")

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = UserForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)

            new = False
            if not o.id:
                new = True

            o.save()
            form.save_m2m()

            #Sets company to current_user company
            if not o.get_company():
                o.set_company()

            if new:
                #send new generated password to the new user
                generate_new_password_for_user(o)

                #Add the new user to allemployee group of the company
                if Core.current_user().get_company_allemployeesgroup():
                    Core.current_user().get_company_allemployeesgroup().add_member(o)

            request.message_success(msg)
            #Redirects after save for direct editing
            return redirect(overview)

    else:
        form = UserForm(instance=instance)

    return render(request, "admin/users/form.html",
                  {'title': _("User"), 'userCard': instance, 'form': form})
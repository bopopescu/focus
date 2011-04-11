# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from app.admin.forms import UserProfileForm, UserProfileImageForm, UserProfilePasswordForm
from core.shortcuts import render_with_request

def edit(request):
    try:
        instance = request.user
        msg = _("Successfully changed your profile")
    except:
        request.message_error(_("Unknown profile"))
        return redirect("/")

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            request.message_success(msg)
            return redirect(edit)
    else:
        form = UserProfileForm(instance=instance, initial={"profileImage": None})

    return render_with_request(request, "admin/profile/form.html", {'title': _('Profile'), 'form': form})


def change_profile_image(request):
    try:
        instance = request.user
        msg = _("Successfully changed profile image")
    except:
        request.message_error(_("Unknown profile"))
        return redirect("/")

    if request.method == 'POST':
        form = UserProfileImageForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            request.message_success(msg)
            return redirect(edit)
    else:
        form = UserProfileImageForm(instance=instance, initial={"profileImage": None})

    return render_with_request(request, "admin/profile/formimage.html", {'title': _('Profile'), 'form': form})


def change_password(request):
    if request.method == 'POST':
        form = UserProfilePasswordForm(request.POST, user=request.user)

        if form.is_valid():
            u = request.user
            u.set_password(form.cleaned_data['new_password'])
            u.save()

            request.message_success(_("Successfully edited password"))

            return redirect(edit)

    else:
        form = UserProfilePasswordForm(user=request.user)

    return render_with_request(request, "admin/profile/formpassword.html",
                               {"title": _("Change password"), 'form': form})
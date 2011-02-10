# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from app.admin.forms import *
from core.shortcuts import *
from core.models import User
from django.utils.translation import ugettext as _

def edit(request):
    return form(request)

def form (request):
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
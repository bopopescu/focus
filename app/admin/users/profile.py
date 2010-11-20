# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required

from core.models import *
from app.admin.forms import *
from core.shortcuts import *
from core.views import updateTimeout
from django.contrib import messages

from django.db.models import Q

@login_required
def edit(request):
    return form(request)


@login_required
def form (request):

    try:
        instance = get_object_or_404(UserProfile, user=request.user)
        msg = "Velykket endret profil"
    except:
        messages.info(request, "Profil finnes ikke")
        return redirect("/")

    #Save and set to active, require valid form
    if request.method == 'POST':

        form = UserProfileForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            messages.success(request, msg)

            #Redirects after save for direct editing
            return redirect("/")

    else:
        form = UserProfileForm(instance=instance)

    #print sendGeneratedPassword(request, 10)

    return render_with_request(request, "form.html", {'title':'Profil', 'form': form })
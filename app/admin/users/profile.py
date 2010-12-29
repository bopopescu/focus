# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from app.admin.forms import *
from core.shortcuts import *
from core.models import User

def edit(request):
    return form(request)

def form (request):

    try:
        instance = request.user
        msg = "Velykket endret profil"
    except:
        request.message_error("Profil finnes ikke")
        return redirect("/")

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            request.message_success(msg)

            #Redirects after save for direct editing
            return redirect("/")

    else:
        form = UserProfileForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Profil', 'form': form})
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse

from app.admin.forms import *
from core.shortcuts import *
from core.views import updateTimeout
from django.contrib import messages
from django.db.models import Q
from core.decorators import login_required, login_required
from core.models import User

#@login_required()
def edit(request):
    return form(request)


#@login_required()
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

    return render_with_request(request, "form.html", {'title':'Profil', 'form': form })
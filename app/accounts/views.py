# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, logout, login as auth_login
from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from core.middleware import get_current_user
from core.models import Log
from django.contrib.auth.models import User

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        redirect_to = request.REQUEST.get('next', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:

                if user.get_profile().canLogin:
                    auth_login(request, user)
                    if not redirect_to:
                        return HttpResponseRedirect("/dashboard/")
                    return HttpResponseRedirect('%s' % redirect_to)
                Log(message = "%s forsøkte å logge inn, men er sperret!" % user).save(user=user)
                return render_to_response('login.html')
        try:
            user  = User.objects.get(username=username)
            Log(message = "%s forsøkte å logge inn" % user).save(user=user)
        except:
            pass

    return render_to_response('login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login/")
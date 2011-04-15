# -*- coding: utf-8 -*-
from core import Core
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from core.auth.user.models import User
from core.auth.log.models import Log

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        redirect_to = request.REQUEST.get('next', '')

        if Core.login(request, username, password):
            user = User.objects.get(username=username)

            if user.canLogin:
                if not redirect_to:
                    return HttpResponseRedirect("/dashboard/")
                return HttpResponseRedirect('%s' % redirect_to)
            Log(message="%s forsøkte å logge inn, men er sperret!" % user).save(user=user)
            return render_to_response('login.html')

        else:
            try:
                user = User.objects.get(username=username)
                Log(message="%s forsøkte å logge inn, men brukte feil passord." % user).save(user=user)
            except:
                pass

    return render_to_response('login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login/")


def logout (request):
    Core.logout(request)
    return redirect('/')
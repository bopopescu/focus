# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, logout, login as auth_login
from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from core.middleware import get_current_user
from core.models import Log
from django.contrib.auth.models import User
from core import Core
from core.shortcuts import render_with_request

"""
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
                    Log(message = "%s logget inn.." % user).save(user=user)
                    if not redirect_to:
                        return HttpResponseRedirect("/dashboard/")
                    return HttpResponseRedirect('%s' % redirect_to)
                Log(message = "%s forsøkte å logge inn, men er sperret!" % user).save(user=user)
                return render_to_response('login.html')
        try:
            user  = User.objects.get(username=username)
            Log(message = "%s forsøkte å logge inn, men bruke felt passord." % user).save(user=user)
        except:
            pass

    return render_to_response('login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login/")

"""



def login (request):

    # If next page is defined, use that instead of the default
    next = request.GET.get('next', '/')

    # Attempt to log in. If successful, redirect to the next page, if not, show error
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            if Core.login(request, data['username'], data['password'], data['remember']):
                return redirect(next)

            else:
                request.message_error("Feil brukernavn og/eller passord, vennligst prøv igjen, eller be om ny passord :)")

        else:
            request.message_error('Du må fylle ut både brukernavn og passord!')
    else:
        form = LoginForm()

    return render_with_request(request, 'user/login.html', {'login_form': form})

def logout (request):

    Core.logout(request)
    request.message_success('Du er nå logget ut!')

    return redirect('/')
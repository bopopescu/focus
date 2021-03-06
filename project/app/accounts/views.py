# -*- coding: utf-8 -*-
from app.accounts.forms import LoginForm
from core import Core
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from core.auth.user.models import User
from core.auth.log.models import Log
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils import translation
from core.decorators import login_required

def login(request):
    message = ""

    redirect_to = request.REQUEST.get('next', '')

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data['username']
            password = data['password']
            remember = data['remember']
            

            if Core.login(request, username, password, remember):
                user = request.user

                if user.canLogin:

                    user.use_user_language(request)

                    Log(message="%s logget inn." % user).save(user=user)

                    if not redirect_to:
                        return HttpResponseRedirect("/dashboard/")

                    return HttpResponseRedirect('%s' % redirect_to)
                
                Log(message="%s forsøkte å logge inn, men er sperret!" % user).save(user=user)
                return render_to_response('login.html')

            else:
                try:
                    user = User.objects.get(username=username)
                    Log(message="%s forsøkte å logge inn, men brukte feil passord." % user).save(user=user)
                except Exception, err:
                    Log(message="ErrorLogin: %s, username: %s" % (err, username)).save()

            Log(message="Attempt to login width username: %s, password: %s, redirect_to: %s, but failed" % (
                username, "******", redirect_to)).save()

        message = _("Wrong username or password")
    else:
        form  = LoginForm()

    return render_to_response('login.html', {'form':form, 'message':message, 'LOGIN_URL': settings.LOGIN_URL})

@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login/")


def logout (request):
    Core.logout(request)
    return redirect('/')
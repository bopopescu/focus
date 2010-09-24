from django.contrib.auth import authenticate, logout, login as auth_login
from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        redirect_to = request.REQUEST.get('next', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                if not redirect_to:
                    return HttpResponseRedirect("/dashboard/")  
                return HttpResponseRedirect('%s' % redirect_to)

    return render_to_response('login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login/")  
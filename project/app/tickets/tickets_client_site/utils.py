import functools
from core.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def client_login_required(view):
    def check_login(request, *args, **kwargs):
        if request.session.get('client_id'):
            return view(request, *args, **kwargs)
        else:
            return redirect(reverse("client_login"))

    functools.update_wrapper(check_login, view  )
    return check_login


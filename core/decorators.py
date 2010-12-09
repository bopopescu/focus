
from functools import wraps
from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.http import Http404

#Require permission in views
from app.dashboard.views import overview

def require_perm(perm, model, objID=False):
    def decorator(func):

        def inner_decorator(request, *args, **kwargs):
            if not len(args):
                return HttpResponseRedirect("/")

            
            if objID:
                obj = model.objects.get(objID=args[0])

                if request.user.has_perm(perm, obj):
                    return func(request, *args, **kwargs)

            else:
                request.message_error("Ingen tilgang!")

                return overview(request)

        return wraps(func)(inner_decorator)
    
    return decorator

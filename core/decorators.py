from functools import wraps
from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.http import Http404

#Require permission in views
def require_perm(perm, model):    
    def decorator(func):

        def inner_decorator(request, *args, **kwargs):
            if not len(args):
                return HttpResponseRedirect("/")
            
            obj = model.objects.get(pk=args[0])
                        
            if request.user.has_perm(perm, obj):
                return func(request, *args, **kwargs)
            else:
                messages.error(request, "Ingen tilgang!")
                return HttpResponseRedirect("/")
        
        return wraps(func)(inner_decorator)
    
    return decorator
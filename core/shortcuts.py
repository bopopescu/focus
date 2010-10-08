from core.models import *
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

def render_with_request(request, template, values = {}, *args, **kwargs):
    """
    Shortcut for render_to_response with context_instance = RequestContext(request))
    Puts things like messages and the user variable in the template
    See also: Django RequestContexts
    """
    
    context_instance = RequestContext(request)
    return render_to_response(template, values, context_instance, *args, **kwargs)
    #return render_to_response(template, values, *args, context_instance = RequestContext(request), **kwargs)
# -*- coding: utf-8 -*-
from django import http
from django.template import   loader
from django.template import RequestContext
from django.shortcuts import _get_queryset, render_to_response, get_object_or_404
from django.core.context_processors import request
from django.http import HttpResponse, Http404
from app.projects.models import Project

def render_with_request(request, template, values={}, *args, **kwargs):
    """
    Shortcut for render_to_response with context_instance = RequestContext(request))
    Puts things like messages and the user variable in the template
    See also: Django RequestContexts
    """

    context_instance = RequestContext(request)
    return render_to_response(template, values, context_instance, *args, **kwargs)


def standardError(request, msg=""):

    if msg == "":
        msg = "Det du leter etter er slettet eller så har du ikke tilgang!"

    return render_with_request(request, 'deletedOrNoPermission.html', {'msg':msg, })


def get_object_or_error(request, klass, *args, **kwargs):

    """
    if get_k(klass, *args, **kwargs):
        return HttpResponse("OK")
    else:
    """
    standardError(request)

    raise ExH(request)
    #return Project.objects.get(id=4)
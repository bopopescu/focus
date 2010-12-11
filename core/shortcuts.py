# -*- coding: utf-8 -*-
from django import http
from django.template import   loader
from django.template import RequestContext
from django.shortcuts import _get_queryset, render_to_response, get_object_or_404
from django.core.context_processors import request
from django.http import HttpResponse, Http404
from app.projects.models import Project
from core.models import User
from core import Core

def render_with_request(request, template, values={}, *args, **kwargs):
    context_instance = RequestContext(request)
    return render_to_response(template, values, context_instance, *args, **kwargs)


"""
Returns users in the same company as the current user
"""
def get_company_users():
    return User.objects.filter(company = Core.current_user())
# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import  render_to_response
from core import Core
from core.models import User

def render_with_request(request, template, values={}, *args, **kwargs):
    context_instance = RequestContext(request)
    return render_to_response(template, values, context_instance, *args, **kwargs)


"""
Returns users in the same company as the current user
"""
def get_company_users():
    return User.objects.filter(company=Core.current_user())
from django.core.cache import cache
import functools
import os, sys, random
from django.contrib.contenttypes.models import ContentType

from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.utils.html import conditional_escape

def get_content_type_for_model(model):

    try:
        model_name = model.__name__
    except Exception, e:
        model_name = model.__class__.__name__

    cache_key = "%s_%s" % ("content_type", model_name)

    if cache.get(cache_key):
        content_type = cache.get(cache_key)
    else:
        content_type = ContentType.objects.get_for_model(model)
        cache.set(cache_key, content_type)

    return content_type


def get_class(app, model):
    content_type = ContentType.objects.get(app_label=app, model=model)
    model = content_type.model_class()
    return model

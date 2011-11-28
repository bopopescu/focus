from django.core.cache import cache
import functools
import os, sys, random
from django.contrib.contenttypes.models import ContentType

from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.utils.html import conditional_escape


content_types = {}

def get_content_type_for_model(model):

    try:
        model_name = model.__name__
    except Exception, e:
        model_name = model.__class__.__name__

    if model_name in content_types:
        return content_types[model_name]

    content_type = ContentType.objects.get_for_model(model)

    content_types[model_name] = content_type

    return content_type

def get_class(app, model):
    content_type = ContentType.objects.get(app_label=app, model=model)
    model = content_type.model_class()
    return model

from operator import attrgetter


class FocusList(list):

    def get(self, id):
        for obj in self:
            if obj.id == id:
                return obj
            return None

    def filter(self, **kwargs):
        result = []

        for obj in self:
            for key,val in kwargs.items():
                if val == getattr(obj, key):
                    result.append(obj)

        return FocusList(result)

    def order_by(self, *args):
        self.sort(key = attrgetter(*args))
        return self
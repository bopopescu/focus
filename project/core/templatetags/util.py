import urllib
from django import template
from django.contrib.contenttypes.models import ContentType
from core.views import get_postal_by_zip
import json


register = template.Library()

def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')

def postal_by_zip(text):
    return get_postal_by_zip(text)

register.filter(url_target_blank)
register.filter(postal_by_zip)
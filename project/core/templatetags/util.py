from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()

def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')

register.filter(url_target_blank)
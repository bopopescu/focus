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

def get_variable (path, i = 1):
    """
    Gets a variable based on the full path of it, e.g. app.event.urls.menu
    """

    import inspect

    # Creates the import "from app.event.urls import menu" from the string "app.event.urls.menu"
    modules = path.split(".")

    try:
        exec("from %s import %s" % (".".join(modules[:-i]), modules[-i]))
    except ImportError as e:

        # If path is a.b.c, and 'from a.b import c' didn't work, try 'from a import b'
        if i < len(modules):
            return get_variable(path, i+1)
        else:
            raise e

    # Return the correct variable, no matter the import
    # If the path is a.b.c, and we used 'from a import b', we have to return b.c
    result = locals()

    while (i > 0):
        if not isinstance(result, dict):
            result = dict(inspect.getmembers(result))

        try:
            result = result[modules[-i]]
        except KeyError:
            # This error might seem a bit weird when you get it, and you don't quite know what this function does,
            # but just trust it! :)
            raise ImportError ("Something is wrong with or in the file %s, python failed to import it! Does the file/function even exist?" % path)

        i -= 1


    return result

def get_permission (view):
    """
    Gets the required permissions on a view, if it is decorated with a require_permission decorator
    returns (None, None) or a tuple (action, object)

    Does *NOT* give back which parameter the decorator has to check,
    it only operates on global permission, at the moment

    view: The full name of the view to get info from, e.g. app.event.views.common.overview
    """

    if not callable(view):
        view = get_variable(view)

    if not hasattr(view, "__decorators__"):
        return (None, None)

    if not 'require_permission' in view.__decorators__:
        return (None, None)

    req = view.__decorators__['require_permission']

    return (req.action, req.model)


class suggest_ajax_parse_arguments:
    """
    Decorator used for view authorization

    Usage:
        Adds query string and limit arguments to a view with this argument,
       error conditions releated to parsing the argumetns

       i.e.
       @suggest_ajax_parse_arguments()
       def autocomplete(request, query, limit):

    Params:
        argument_name - name of the parameter which has the argument
        default_limit - default limit on how many results that should be returned
        limit_name -    name on the limit parameter deciding the limit on how many
                        results that should be returned
    """

    def __init__(self, argument_name = 'term', default_limit = 15, limit_name = 'limit'):
        """
        Used to make ajax-suggest views simpler
        Called when python finds a decorator
        """
        self.argument_name = argument_name
        self.default_limit = default_limit
        self.limit_name = limit_name

    def __call__(self, func):
        """
        Used to make ajax-suggest views simpler
        Called when a method we have decorated is called
        """

        def check_arguments (request, *args, **kwargs):
                if not request.GET.get(self.argument_name):
                    return HttpResponse(mimetype='text/plain')

                query = request.GET.get(self.argument_name)
                limit = request.GET.get(self.limit_name, self.default_limit)
                try:
                    limit = int(limit)
                except ValueError:
                    return HttpResponseBadRequest()

                return func(request, query, limit, *args, **kwargs)

        functools.update_wrapper(check_arguments, func)
        return check_arguments
#       functools.update_wrapper(check_permission, func)
#        return check_permission
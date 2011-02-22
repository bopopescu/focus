import functools
import os, sys, random

from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.utils.html import conditional_escape

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
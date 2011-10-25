from django.conf import settings
from django.core.cache import cache
import functools

"""
Cache framework
"""

class cachedecorator:

    label = ""

    def __init__(self, label, timeout = False):
        """
        Used for decorator caching
        Called when python finds a decorator
        """

        self.label = label

    def __call__(self, func):
        """
        Used for decorator caching
        Called when a method we have decorated is called
        """

        def cache_function (*args, **kwargs):

            
            cache_key = "cachedecorator_%s_%s_%s" % (args[0].__class__.__name__, args[0].pk, self.label)
            cached = cache.get(cache_key)

            if cached is not None:
                return cached
            else:
                print "%s : %s " % (cache_key, cached)
                value = func(*args, **kwargs)
                cache.set(cache_key, value)
                return value

        functools.update_wrapper(cache_function, func)
        return cache_function
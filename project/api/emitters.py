from django.core.cache import cache
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.utils import simplejson
from piston.emitters import Emitter
from core import Core

class JSONCachedEmitter(Emitter):
    """
    JSON emitter that caches the response for a given request
    """

    def render(self, request):
        cache_key = str(Core.current_user().id) + request.path + request.META['QUERY_STRING']
        old = cache.get(cache_key)
        if old:
            return old
        seria = simplejson.dumps(self.construct(), cls=DateTimeAwareJSONEncoder, ensure_ascii=False, indent=4)
        cache.set(cache_key, seria)
        return seria

Emitter.register('json-cached', JSONCachedEmitter, 'application/json; charset=utf-8')
            
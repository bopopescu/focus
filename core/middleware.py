# cciw/middleware/threadlocals.py
import threading
from django.shortcuts import HttpResponseRedirect

from django.contrib.auth.models import User, UserManager, Group

"""
This is used for getting the current user, so it can be reached from anywhere, an model for instance.
This is useful.
"""

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)


def get_company_users(): 
    company = get_current_user().get_profile().company
    users = User.objects.filter(userprofile__company = company)
    return users

class ThreadLocals(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)
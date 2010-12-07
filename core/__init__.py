
import hashlib, os, threading, inspect
from datetime import datetime, timedelta

from django.db.models import signals, Q
from django.template import RequestContext
from django.conf import settings
from core.models import User


class Core:
    """
    Core user functions

    Authentication, login and logout, should be pretty self-explanatory

    Attaching and detaching users is done to make NERD thread-safe; it associates
    the current user to the thread it's in, making sure users aren't mistaken for each other.
    The middleware is responsible for attaching and detaching every request.
    """

    """The users dict should be protected by the userlock at all times"""
    users = {}

    # lock used for only givng one hread at a time access to users
    lock = threading.RLock()

    @classmethod
    def current_user (cls):
        """
        returns the user associated with the current request
        """

        thread = threading.currentThread()

        with cls.lock:
            if thread in cls.users:
                return cls.users[thread]

        return False

    @classmethod
    def attach_user (cls,request):
         """
         attach user to thread
         """
         thread = threading.currentThread()
         with cls.lock:
            cls.users[thread] = Core._get_user(request)

    @classmethod
    def detach_user(cls):
        thread = threading.currentThread()
        with cls.lock:
            cls.users.pop(thread, None)


    @staticmethod
    def authenticate (username, password):
        """
        Returns True if the user/password combination exists
        """

        try:
            user = User.objects.get(username = username)
            if user.check_password(password):
                return user
            else:
                return False

        except:
            return False


    @staticmethod
    def login(request, username, password):
        """
        Logs inn with the given username and password
        """

        user = Core.authenticate(username, password)

        if user:
            request.session['user_id']  = user.pk
            request.user = user

            Core.attach_user(request)

        else:
            return False


    @staticmethod
    def logout(request):
        """
        Logs out the user
        """
        request.session.pop('user_id', None)
        request.user = None



def load_initial_data(app, sender, **kwargs):
    """
    Load the initial data for all models on syncdb
    """
    if hasattr(sender, 'initial_data'):
        origin = inspect.getmodule(sender.initial_data)

        if sender == origin:
            print "Loading %s initial data" % sender.__name__
            print "=" * 50
            sender.initial_data()
            print "=" * 50
            print ""

        else:
            print "WARNING: The initial_data function from %s was imported by %s. Are you importing %s.* ? Stop that!" % (origin.__name__, sender.__name__, origin.__name__)

signals.post_syncdb.connect(load_initial_data)
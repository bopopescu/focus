# -*- coding: utf-8 -*-
import threading, inspect
from datetime import datetime
from south import signals
from django.conf import settings

class Core:
    """
    Core user functions

    Authentication, login and logout, should be pretty self-explanatory

    Attaching and detaching users is done to make it thread-safe; it associates
    the current user to the thread it's in, making sure users aren't mistaken for each other.
    The middleware is responsible for attaching and detaching every request.
    """

    # The users dict should be protected by the lock at all times
    users = {}

    # Lock used for only giving one thread at a time access to users
    lock = threading.RLock()

    # Used in testing
    test_user = None

    @classmethod
    def current_user (cls):
        """
        Returns the user associated with the current thread/request
        """

        if cls.test_user:
            return cls.test_user

        thread = threading.currentThread()

        with cls.lock:
            if thread in cls.users:
                return cls.users[thread]


        return AnonymousUser()

    @classmethod
    def attach_user (cls, request):
        """
        Attaches a user to a thread
        """

        thread = threading.currentThread()

        with cls.lock:
            cls.users[thread] = Core._get_user(request)


    @classmethod
    def detach_user (cls):
        """
        Detaches a user connected to a thread
        """

        thread = threading.currentThread()

        with cls.lock:
            cls.users.pop(thread, None)

    @staticmethod
    def authenticate (username, password):
        """
        Returns True if the user/password combination exists
        """
        try:
            user = User.objects.get(username=username)

            if user.check_password(password):
                return user
            else:
                return False

        except:
            return False

    @staticmethod
    def login (request, username, password, remember=False):
        """
        Logs in with the given username/password
        Returns True and logs the user in if username/password is correct, False otherwise
        """

        user = Core.authenticate(username, password)

        if user:
            request.session['user_id'] = user.pk
            request.user = user
            Core.attach_user(request)

            # Remember me if I tell you to!
            if remember:
                key, created = UserLoginKey.objects.get_or_create(user=user,
                                                                  ip=request.META['REMOTE_ADDR'])

                key.last_login = datetime.now()
                key.save(log=False)

                request.set_cookie('username', user.username, max_age=settings.LOGIN_REMEMBER_TIME);
                request.set_cookie('userkey', key.key, max_age=settings.LOGIN_REMEMBER_TIME);

            return True

        return False

    @staticmethod
    def logout (request):
        """
        Logs out the current user
        """
        # Delete the cookie and cookie key key for this IP
        if 'userkey' in request.COOKIES:
            keys = UserLoginKey.objects.filter(user=request.user,
                                               key=request.COOKIES['userkey'],
                                               ip=request.META['REMOTE_ADDR'])

            for key in keys:
                key.delete(log=False)

            request.delete_cookie('username')
            request.delete_cookie('userkey')

        request.session.pop('user_id', None)
        request.user = None

    @classmethod
    def set_test_user (cls, user):
        """
        Used in tests to set the current user
        """

        cls.test_user = user


    @staticmethod
    def _get_user (request):
        """
        Retrieves the currently logged in user, or None if the user is not logged in
        Don't use this externally, use current_user, as it's thread safe
        """

        if not 'user_id' in request.session:
            return None

        try:
            user = User.objects.get(pk=request.session['user_id'])
        except User.DoesNotExist:
            user = AnonymousUser()

        return user


def load_initial_data(app, **kwargs):
    """
    Load the initial data for all models on syncdb
    """

    try:
        module = __import__('app.%s.models' % app, fromlist = 1)
    except ImportError:
        try:
            module = __import__('%s.models' % app, fromlist = 1)
        except ImportError:
            return

    if hasattr(module, 'initial_data'):
        print "Loading %s initial data" % app
        print "=" * 50
        module.initial_data()
        print "=" * 50
        print ""

signals.post_migrate.connect(load_initial_data)

from core.auth.user.models import AnonymousUser, User
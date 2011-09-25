from core import Core
from functools import partial
from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils import translation

class CookieMiddleware (object):
    """
    Django doesn't allow setting cookies on a request, only on a response.
    Let's change that! Adds set_cookie and delete_cookie to request, and then sets/deletes the cookie
    in the response afterwards.

    The syntax is the same for request.set_cookie as for response.set_cookie
    """

    def process_request (self, request):

        request.new_cookies = []
        request.delete_cookies = []

        request.set_cookie = partial(self.set_cookie, request)
        request.delete_cookie = partial(self.delete_cookie, request)

        return None

    def process_response (self, request, response):

        # If cookie process_request was not run, don't bother with the cookies
        if not hasattr(request, 'new_cookies'):
            return response

        for args, kwargs in request.new_cookies:
            response.set_cookie(*args, **kwargs)

        for args, kwargs in request.delete_cookies:
            response.delete_cookie(*args, **kwargs)

        return response

    def set_cookie (self, request, *args, **kwargs):

        request.new_cookies.append((args, kwargs))

    def delete_cookie (self, request, *args, **kwargs):

        request.delete_cookies.append((args, kwargs))

class AuthenticationMiddleware (object):
    """
    Attach currently logged in user to the request
    CookieMiddleware has to be init'ed over this.
    """

    def process_request (self, request):

        # Save the current thread with the current user
        Core.attach_user(request)
        request.user = Core.current_user()

        return None

    def process_response (self, request, response):

        # Detach the thread/user association, if any
        Core.detach_user()
        return response

    def process_exception (self, request, exception):

        # Detach the thread/user association, if any, in case of an exception
        Core.detach_user()
        return None

class MessageMiddleware (object):
    """
    Attaches a message function to the request, enabling an easy way of
    reporting stuff back to the user
    """

    def process_request (self, request):

        # Uses a partial function to feed the request
        request.message_success = partial(self.add_message, request, "success")
        request.message_error = partial(self.add_message, request, "error")
        request.message_info = partial(self.add_message, request, "info")

        return None

    @staticmethod
    def add_message (request, type, message):
        """
        Adds a message to the request, so we can show it again at the next screen
        The type can be used for the css-class in the code,
        so add_message(request, "error", "It failed :(") generates something looking like an error :)
        """

        if not 'messages' in request.session:
            request.session['messages'] = []

        msg = {'text': message,
               'type': type}

        request.session['messages'].append(msg)


    @staticmethod
    def get_messages (request):
        """
        Get the messages waiting for this request
        """
        
        if not 'messages' in request.session:
            request.session['messages'] = []

        messages = request.session['messages']
        request.session['messages'] = []

        return messages


class SessionBasedLocaleMiddleware(object):
    """
    This Middleware saves the desired content language in the user session.
    The SessionMiddleware has to be activated.
    """
    def process_request(self, request):
        if request.method == 'GET' and 'lang' in request.GET:
                language = request.GET['lang']
                request.session['language'] = language
        elif 'language' in request.session:
                language = request.session['language']
        else:
                language = translation.get_language_from_request(request)

        for lang in settings.LANGUAGES:
            if lang[0] == language:
                translation.activate(language)

        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response
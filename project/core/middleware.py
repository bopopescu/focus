from core import Core
from functools import partial
from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils import translation

class AuthenticationMiddleware(object):
    """
    Log in someone who has said to remember him/her.
    Also the currently logged in user to the request

    CookieMiddleware has to be init'ed over this.
    """

    def process_request (self, request):
        user = Core._get_user(request)

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

class MessageMiddleware(object):
    """
    Attaches a message function to the request, enabling an easy way of
    reporting stuff back to the user
    """

    def process_request (self, request):

    # Uses a partial function to feed the request
        request.message_success = partial(self.add_message, request, "success")
        request.message_error = partial(self.add_message, request, "fail")
        request.message_info = partial(self.add_message, request, "info")

        return None

    @staticmethod
    def add_message (request, type, message):
        """
        Adds a message to the request, so we can show it again at the next screen
        The type can be used for the css-class in the code,
        so add_message(request, "error", "It failed :(") generates something looking like an error :)
        """
        request.session['DFSDF'] = "HEI"

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
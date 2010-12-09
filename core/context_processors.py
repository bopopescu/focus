from core.middleware import MessageMiddleware
import settings

def message (request):
    """
    Puts the messages from the message middleware in the
    RequestContext object, for use in the template
    """

    return {'messages': MessageMiddleware.get_messages(request)}


def user (request):
    """
    Puts the currently logged in user and the login form in the
    RequestContext object, for use in the template
    """

    return {'user': request.user,
            'debug': settings.DEBUG}
from core import Core
from core.auth.user.models import User
from django.http import HttpResponse

class TimeBasicAPIAuthentication(object):
    def __init__(self):
        self.realm = "TIME API"

    def is_authenticated(self, request):
        #Check if already logged in, for use inside the application
        if Core.current_user() and Core.current_user().is_authenticated():
            return True

        #If not, then use basic auth
        else:
            auth_string = request.META.get('HTTP_AUTHORIZATION', None)

            if not auth_string:
                return False

            (authmeth, auth) = auth_string.split(" ", 1)

            if not authmeth.lower() == 'basic':
                return False

            auth = auth.strip().decode('base64')
            (username, password) = auth.split(':', 1)

            if Core.login(request, username, password):
                user = User.objects.get(username=username)
                return user.canLogin

        return False

    def challenge(self):
        resp = HttpResponse("Authorization Required")
        resp['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
        resp.status_code = 401
        return resp
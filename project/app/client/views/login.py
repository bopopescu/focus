from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from app.client.models import ClientUser
from core.mail import send_mail
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.utils import simplejson

def login(request):
    error = False
    if request.method == 'POST':
        try:
            client = ClientUser.objects.get(email=request.POST['email'])
        except ClientUser.DoesNotExist:
            client = None

        if client and client.check_password(request.POST['password']):
            request.session['client_id'] = client.id
            return redirect(reverse('app.client.views.tickets.overview'))

        error = True

    return render(request, "client/login.html", {'error': error})

def logout(request):
    try:
        del request.session['client_id']
    except KeyError:
        pass
    return redirect(reverse("login.client_login"))



def new_password(request):
    if request.is_ajax() and request.method == 'POST':
        email = request.POST['email']
        ret = {'error': False}
        print ret
        try:
            client = ClientUser.objects.get(email=email)
            pwd = ClientUser.generate_password()
            client.set_password(pwd)
            client.save()
            send_mail(_('New Password'), _('Your new password is: ') + '%s' % pwd,
                      settings.NO_REPLY_EMAIL, [email], fail_silently=False)
            ret['text'] = _('New password sent')
        except ClientUser.DoesNotExist:
            ret['error'] = True
            ret['text'] = _('Email not found')
        return HttpResponse(simplejson.dumps(ret), mimetype='application/javascript')
    else:
        return HttpResponse(status=404)

    

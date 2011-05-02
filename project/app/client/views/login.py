from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from app.client.models import ClientUser

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
    return redirect(reverse("client_login"))
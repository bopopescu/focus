from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required

from core.models import *
from app.admin.forms import *
from core.shortcuts import *
from core.views import updateTimeout
from django.contrib import messages

from django.db.models import Q

@login_required
def overview(request):
    updateTimeout(request)
    Company = request.user.get_profile().company
    Users = User.objects.filter(userprofile__company=Company)
    return render_with_request(request, 'admin/users/list.html', {'title':'Brukere', 'users':Users})

@login_required
def grant_permissions(request):
    Users = User.objects.all()    
    Permissions = Permission.objects.all()
    return render_with_request(request, 'admin/users/grant_permssions.html', {'title':'Brukere', 'users':Users, 'permissions':Permissions })

def add(request):
    return form(request)

@login_required
def edit(request, id):
    return form(request, id)

@login_required
def editProfile(request):
    pass

@login_required
def sendGeneratedPassword(request, userID):

    user = get_object_or_404(User, id = userID, userprofile__company = request.user.get_profile().company)

    import string
    import random

    vowels = ['a','e','i','o','u']
    consonants = [a for a in string.ascii_lowercase if a not in vowels]
    ret = ''
    slen = 8

    for i in range(slen):
        if i%2 ==0:
            randid = random.randint(0,20) #number of consonants
            ret += consonants[randid]
        else:
            randid = random.randint(0,4) #number of vowels
            ret += vowels[randid]

    ret += "%s" % random.randint(20,99)

    from django.core.mail import send_mail

    send_mail('Nytt passord', 'Nytt passord er: %s' % ret, 'FocusTime',
        ["%s"%user.email], fail_silently=True)

    user.set_password("%s"%ret)
    user.save()

    messages.success(request, "Velykket sendt nytt passord til epost")

    return redirect(overview)

def get_permissions(user):
    Permissions = ObjectPermission.objects.filter(
                                                  (
                                                   
                                                   #Q(content_type__fabelf="K") &
                                                   
                                                   (
                                                    Q(user=user) 
                                                    |
                                                    Q(membership__in=user.memberships.all))
                                                  )
                                                ).order_by('content_type')
    return Permissions
    

@login_required
def addPop(request):
    instance = User()
    
    if request.method == "POST": 

        form = UserForm(request.POST, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                            ((o._get_pk_val()), (o)))
            
    else:
        form = UserForm(instance=instance)
    
    return render_with_request(request, "simpleform.html", {'title':'Bruker', 'form': form })
  
  
@login_required
def view(request, id):
    user = User.objects.get(id=id)
    Permissions = get_permissions(user)
    
    return render_with_request(request, 'admin/users/view.html', {'title':'Bruker',
                                                                  'user':user,
                                                                  'permissions':Permissions,
                                                                  })
@login_required
def delete(request, id):
    messages.success(request, "Velykket slettet bruker")        
    return redirect(overview)

@login_required
def form (request, id = False):        

    if id:
        instance = get_object_or_404(User, id = id, userprofile__company = request.user.get_profile().company)
        msg = "Velykket endret bruker"
    else:
        instance = User()
        msg = "Velykket lagt til ny bruker"

    #Save and set to active, require valid form
    if request.method == 'POST':
        
        form = UserForm(request.POST, instance=instance)

        if form.is_valid():    
            o = form.save(commit=False)

            o.save()
            form.save_m2m()

            if not o.get_profile().company:
                o.get_profile().company = request.user.get_profile().company
                o.get_profile().save()

            messages.success(request, msg)

            #Redirects after save for direct editing
            return redirect(overview)   

    else:
        form = UserForm(instance=instance)

    #print sendGeneratedPassword(request, 10)

    return render_with_request(request, "form.html", {'title':'Bruker', 'form': form })
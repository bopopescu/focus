from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required

from core.models import *
from app.admin.forms import *
from core.shortcuts import *

from django.contrib import messages

from django.db.models import Q

@login_required
def overview(request):
    Company = request.user.get_profile().company
    Users = User.objects.filter(userprofile__company=Company)
    return render_with_request(request, 'admin/list.html', {'title':'Brukere', 'users':Users})

@login_required
def grant_permissions(request):
    Users = User.objects.all()    
    Permissions = Permission.objects.all()
    return render_with_request(request, 'admin/grant_permssions.html', {'title':'Brukere', 'users':Users, 'permissions':Permissions })

def add(request):
    return form(request)

@login_required
def edit(request, id):
    return form(request, id)

def get_permissions(user, content_type):
    Permissions = ObjectPermission.objects.filter(
                                                  (Q(content_type = ContentType.objects.get_for_model(content_type)) & 
                                                  (Q(user=user)| Q(membership__in=user.memberships.all))
                                                  )
                                                  )

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

    from app.customers.models import Customer
    from app.projects.models import Project
    from app.orders.models import Order
    from app.contacts.models import Contact
    
    CustomerPerm = get_permissions(user, Customer)
    ProjectPerm = get_permissions(user, Project)
    OrderPerm = get_permissions(user, Order)
    ContactPerm = get_permissions(user, Contact)
    
    return render_with_request(request, 'admin/view.html', {'user':user, 
                                                                  'CustomerPerm':CustomerPerm,
                                                                  'ProjectPerm':ProjectPerm,
                                                                  'ContactPerm':ContactPerm,
                                                                  'OrderPerm':OrderPerm})
@login_required
def delete(request, id):
    messages.success(request, "Velykket slettet bruker")        
    return redirect(overview)

@login_required
def form (request, id = False):        

    if id:
        instance = get_object_or_404(User, id = id)
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
                   
            messages.success(request, msg)  
            #Redirects after save for direct editing
            return redirect(overview)   
        
           
    else:
        form = UserForm(instance=instance)
    
    return render_with_request(request, "form.html", {'title':'Kontakt', 'form': form })
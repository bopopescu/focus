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
    Memberships = Membership.objects.for_company()
    return render_with_request(request, 'admin/memberships/list.html', {'title':'Grupper', 'memberships':Memberships})


def add(request):
    return form(request)

@login_required
def edit(request, id):
    return form(request, id)

def get_permissions(membership, content_type):
    Permissions = ObjectPermission.objects.filter(
                                                  (Q(content_type = ContentType.objects.get_for_model(content_type)) & 
                                                  (Q(membership=membership))
                                                  )
                                                )
    return Permissions
    

@login_required
def addPop(request):
    instance = User()
    
    if request.method == "POST": 
        form = MembershipForm(request.POST, instance=instance)
        if form.is_valid():        
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                            ((o._get_pk_val()), (o)))
            
    else:
        form = MembershipForm(instance=instance)
    
    return render_with_request(request, "simpleform.html", {'title':'Bruker', 'form': form })
  
  
@login_required
def view(request, id):
    
    membership = Membership.objects.get(id=id)

    from app.customers.models import Customer
    from app.projects.models import Project
    from app.orders.models import Order
    from app.contacts.models import Contact
    
    CustomerPerm = get_permissions(membership, Customer)
    ProjectPerm = get_permissions(membership, Project)
    OrderPerm = get_permissions(membership, Order)
    ContactPerm = get_permissions(membership, Contact)
    
    return render_with_request(request, 'admin/memberships/view.html', {'membership':membership, 
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
        instance = get_object_or_404(Membership, id = id)
        msg = "Velykket endret gruppe"
    else:
        instance = Membership()
        msg = "Velykket lagt til ny gruppe"
        
    #Save and set to active, require valid form
    if request.method == 'POST':
        
        form = MembershipForm(request.POST, instance=instance)       
        if form.is_valid():    
            o = form.save(commit=False)
            o.save()
            form.save_m2m()
                   
            messages.success(request, msg)  
            #Redirects after save for direct editing
            return redirect(overview)   
        
           
    else:
        form = MembershipForm(instance=instance)
    
    return render_with_request(request, "form.html", {'title':'Gruppe', 'form': form })
from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from models import *
from forms import *
from core.shortcuts import *
from django.contrib import messages
from core.views import *
from core.decorators import *

@login_required
def overview(request):
    orders = Order.objects.all()    
    return render_with_request(request, 'orders/list.html', {'title':'Ordrer', 'orders':orders})

@login_required
def add(request):
    return form(request)

@login_required
def edit(request, id):
    return form(request, id)

@login_required
def delete(request, id):
    return form(request, id)

@login_required
def view(request, id):
    order = Order.objects.for_user().get(id=id)
    return render_with_request(request, 'orders/view.html', {'title':'Ordre: %s' % order.order_name, 
                                                               'order':order})

@login_required
def permissions(request, id):
    type = Order
    url = "orders/edit/%s" % id
    message = "Vellykket endret tilgang for ordre: %s" % type.objects.get(pk=id)
    return form_perm(request, type, id, url, message)


@login_required
def addPop(request):
    instance = Order()
    
    if request.method == "POST": 
        form = OrderFormSimple(request.POST, instance=instance)
        if form.is_valid():    
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                            ((o._get_pk_val()), (o)))
    else:
        form = OrderFormSimple(instance=instance)
            
    return render_with_request(request, "simpleform.html", {'title':'Ordre', 'form': form })

@login_required
def form (request, id = False):
        
    if id:
        instance = get_object_or_404(Order, id = id, deleted=False)
        msg = "Velykket endret ordre"
    else:
        instance = Order()
        msg = "Velykket lagt til nytt ordre"
      

    #Save and set to active, require valid form
    if request.method == 'POST':
    
        form = OrderForm(request.POST, instance=instance)       
        if form.is_valid():    
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            messages.success(request, msg)        
            if not id:      
                return redirect(permissions, o.id)  
            return redirect(overview) 
        
    else:
        form = OrderForm(instance=instance)
    
    return render_with_request(request, "orders/form.html", {'title':'Ordre', 'form': form })
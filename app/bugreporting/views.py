from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required

from models import *
from forms import *
from core.shortcuts import *
from django.contrib import messages

from filetransfers.api import prepare_upload

@login_required
def overview(request):
    Bugreportings = Bug.objects.all()    
    return render_with_request(request, 'bugreporting/list.html', {'title':'Registrerte bugs', 'bugs':Bugreportings})

@login_required
def add(request):
    return form(request)

@login_required
def view(request, id):
    ticket = Bug.objects.get(id=id)
    return render_with_request(request, 'bugreporting/view.html', {'title':ticket.title, 'ticket':ticket})

@login_required
def changeStatus(request, id):
    ticket = Bug.objects.get(id=id)
    ticket.closed = not ticket.closed
    ticket.save()
    return redirect(view, id)
    
@login_required
def edit(request, id):
    return form(request, id)

@login_required
def delete(request, id):
    return form(request, id)

@login_required
def form (request, id = False):        
    
    if id:
        instance = get_object_or_404(Bug, id = id, deleted=False)
        msg = "Velykket endret bug"
    else:
        instance = Bug()
        msg = "Velykket lagt til ny bug"
        
    #Save and set to active, require valid form
    if request.method == 'POST':

        form = BugreportingForm(request.POST, request.FILES, instance=instance)       
        if form.is_valid():    
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            messages.success(request, msg)
            #Redirects after save for direct editing
            return overview(request)      
    else:
        form = BugreportingForm(instance=instance)
        
    return render_with_request(request, "form.html", {'title':'Bugs', 
                                                      'form': form })
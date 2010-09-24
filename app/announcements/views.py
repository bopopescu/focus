from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required

from models import *
from forms import *
from core.shortcuts import *
from core.views import *

@login_required
def overview(request):
    announcements = Announcement.objects.all()    
    return render_with_request(request, 'announcements/list.html', {'title':'Oppslag', 'announcements':announcements})

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
def permissions(request, id):
    type = Announcement
    url = "announcements/edit/%s" % id
    message = "Vellykket endret tilgang for oppslaget: %s" % type.objects.get(pk=id)
    return form_perm(request, type, id, url, message)

@login_required
def form (request, id = False):        

    if id:
        instance = get_object_or_404(Announcement, id = id, deleted=False)
        msg = "Velykket endret oppslag"
    else:
        instance = Announcement()
        msg = "Velykket lagt til ny oppslag"
        
    #Save and set to active, require valid form
    if request.method == 'POST':
        
        form = AnnouncementForm(request.POST, instance=instance)       
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
        form = AnnouncementForm(instance=instance)
    
    return render_with_request(request, "form.html", {'title':'Oppslag', 'form': form })
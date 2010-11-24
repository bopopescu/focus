from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required

from models import *
from forms import *
from core.shortcuts import *
from core.views import *
from core.decorators import require_perm

@login_required
def overview(request):
    announcements = Announcement.objects.for_company()
    return render_with_request(request, 'announcements/list.html', {'title':'Oppslag', 'announcements':announcements})

@login_required
def overview_deleted(request):
    announcements = Announcement.objects.for_company(deleted=True)
    return render_with_request(request, 'announcements/list.html', {'title':'Oppslag', 'announcements':announcements})

@login_required
def add(request):
    return form(request)


@require_perm('view', Announcement)
def view(request, id):
    announcement = get_object_or_404(Announcement, id = id)
    return render_with_request(request, 'announcements/view.html', {'title':'Oppslag',
                                                                    'announcement':announcement})
@require_perm('change', Announcement)
def edit(request, id):
    return form(request, id)

@require_perm('delete', Announcement)
def delete(request, id):
    Announcement.objects.for_company().get(id=id).delete()
    return redirect(overview)

@require_perm('delete', Announcement)
def recover(request, id):
    Announcement.objects.for_company(deleted=True).get(id=id).recover()
    return redirect(overview)

@require_perm('modifyPermissions', Announcement)
def permissions(request, id):
    type = Announcement
    url = "announcements/view/%s" % id
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
        
        form = AnnouncementForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():    
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            messages.success(request, msg)        
            if not id:      
                return redirect(permissions, o.id)  
            return redirect(view, o.id)
             
    else:
        form = AnnouncementForm(instance=instance)
    
    return render_with_request(request, "form.html", {'title':'Oppslag', 'form': form })
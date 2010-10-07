from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.html import escape 
from models import *
from forms import *
from core.shortcuts import *
from core.decorators import *
from core.views import form_perm

@login_required
def overview(request):
    projects = Project.objects.for_user()  
    return render_with_request(request, 'projects/list.html', {'title':'Prosjekter', 'projects':projects})

@login_required
def overview_deleted(request):
    projects = Project.objects.for_company(deleted=True)
    return render_with_request(request, 'projects/list.html', {'title':'Slettede prosjekter', 'projects':projects})

@login_required
def overview_all(request):
    projects = Project.objects.for_company()  
    return render_with_request(request, 'projects/list.html', {'title':'Alle prosjekter', 'projects':projects})


@require_perm('view', Project)
def view(request, id):
    project = Project.objects.for_company().get(id=id)
    whoCanSeeThis = project.whoHasPermissionTo('view')
    return render_with_request(request, 'projects/view.html', {'title':'Prosjekt: %s' % project.name, 
                                                               'project':project,
                                                               'whoCanSeeThis':whoCanSeeThis,
                                                               })
 
@login_required
def addPop(request):
    instance = Project()
    
    if request.method == "POST": 
        form = ProjectForm(request.POST, instance=instance)
        if form.is_valid():    
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()

            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                           (escape(o._get_pk_val()), escape(o)))
            
            
    else:
        form = ProjectForm(instance=instance)
            
    return render_with_request(request, "simpleform.html", {'title':'Prosjekt', 'form': form })

  
@login_required
def add(request):
    return form(request)

@require_perm('change', Project)
def edit(request, id):
    return form(request, id)

@require_perm('delete', Project)
def delete(request, id):
    Project.objects.get(id=id).delete()
    return redirect(overview)

@login_required
def permissions(request, id):
    type = Project
    url = "projects/edit/%s" % id
    message = "Vellykket endret tilgang for prosjektet: %s" % type.objects.get(pk=id)
    return form_perm(request, type, id, url, message)

@login_required
def form (request, id = False):
        
    if id:
        instance = get_object_or_404(Project, id = id, deleted=False)
        msg = "Velykket endret prosjekt"
    else:
        instance = Project()
        msg = "Velykket lagt til nytt prosjekt"
  
    #Save and set to active, require valid form
    if request.method == 'POST':
    
        form = ProjectForm(request.POST, instance=instance)       
        if form.is_valid():    
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            messages.success(request, msg)        
            #Redirects after save for direct editing
            if not id:      
                return redirect(permissions, o.id)  
            return redirect(overview)
        
    else:
        form = ProjectForm(instance=instance)
    
    return render_with_request(request, "form.html", {'title':'Prosjekt', 'form': form })
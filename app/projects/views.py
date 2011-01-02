# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.html import escape
from app.contacts.models import Contact
from forms import *
from core.shortcuts import *
from core.decorators import *
from core.views import updateTimeout

@require_permission("LIST", Project)
def overview(request):
    updateTimeout(request)
    projects = Core.current_user().getPermittedObjects("VIEW", Project)
    return render_with_request(request, 'projects/list.html', {'title': 'Prosjekter', 'projects': projects})

@require_permission("LIST", Project)
def overview_deleted(request):
    projects = Project.objects.all(deleted=True)
    return render_with_request(request, 'projects/list.html', {'title': 'Slettede prosjekter', 'projects': projects})

@require_permission("LIST", Project)
def overview_all(request):
    projects = Project.objects.all()
    return render_with_request(request, 'projects/list.html', {'title': 'Alle prosjekter', 'projects': projects})

@require_permission("VIEW", Project, 'id')
def view(request, id):
    project = Project.objects.get(id=id)
    whoCanSeeThis = project.whoHasPermissionTo('view')
    return render_with_request(request, 'projects/view.html', {'title': 'Prosjekt: %s' % project,
                                                               'project': project,
                                                               'whoCanSeeThis': whoCanSeeThis,
                                                               })

@login_required()
def addPop(request):
    instance = Project()

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()

            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                    (escape(o._get_pk_val()), escape(o)))

    else:
        form = ProjectForm(instance=instance)

    return render_with_request(request, "simpleform.html", {'title': 'Prosjekt', 'form': form})


@require_permission("CREATE", Project)
def add(request):
    return form(request)

@require_permission("EDIT", Project, 'id')
def edit(request, id):
    return form(request, id)

@require_permission("DELETE", Project, 'id')
def delete(request, id):
    Project.objects.get(id=id).delete()
    return redirect(overview)

def form (request, id=False):
    if id:
        instance = get_object_or_404(Project, id=id, deleted=False)
        msg = "Vellykket endret prosjekt"
    else:
        instance = Project()
        msg = "Vellykket lagt til nytt prosjekt"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            request.message_success(msg)

            return redirect(overview)

    else:
        form = ProjectForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Prosjekt', 'form': form})
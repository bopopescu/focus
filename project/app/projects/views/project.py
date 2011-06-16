# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import escape
from app.contacts.models import Contact
from app.projects.forms import ProjectForm, ProjectFormSimple
from app.projects.models import Project
from core import Core
from core.models import Log
from core.shortcuts import comment_block
from core.decorators import require_permission
from core.views import update_timeout
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType

@require_permission("LIST", Project)
def overview(request):
    update_timeout(request)
    projects = Core.current_user().get_permitted_objects("VIEW", Project).filter(trashed=False)
    return render(request, 'projects/list.html', {'title': 'Prosjekter', 'projects': projects})


@require_permission("LIST", Project)
def timeline(request):
    update_timeout(request)
    projects = Core.current_user().get_permitted_objects("VIEW", Project).filter(trashed=False)
    return render(request, 'projects/timeline.html',
                               {'title': 'Tidslinje for alle prosjekter', 'projects': projects})


@require_permission("LIST", Project)
def overview_trashed(request):
    projects = Core.current_user().get_permitted_objects("VIEW", Project).filter(trashed=True)
    return render(request, 'projects/list.html', {'title': 'Slettede prosjekter', 'projects': projects})


@require_permission("LIST", Project)
def overview_all(request):
    projects = Project.objects.all()
    return render(request, 'projects/list.html', {'title': 'Alle prosjekter', 'projects': projects})


@require_permission("VIEW", Project, "id")
def milestones(request, id):
    project = Project.objects.get(id=id)
    return render(request, "projects/milestones.html", {"project": project})


@require_permission("VIEW", Project, 'id')
def view(request, id):
    project = Project.objects.get(id=id)
    comments = comment_block(request, project)
    who_can_see_this = project.who_has_permission_to('view')
    return render(request, 'projects/view.html', {'title': 'Prosjekt: %s' % project,
                                                               'comments': comments,
                                                               'project': project,
                                                               'who_can_see_this': who_can_see_this,
                                                               })


@require_permission("VIEW", Project, 'id')
def view_orders(request, id):
    project = Project.objects.get(id=id)

    return render(request, 'projects/orders.html', {'title': 'Prosjekt: %s orders' % project,
                                                                 'project': project,
                                                                 'orders': project.orders.all(),
                                                                 })


@require_permission("EDIT", Project, "id")
def history(request, id):
    instance = get_object_or_404(Project, id=id, deleted=False)
    history = instance.history()
    return render(request, 'projects/log.html', {'title': _("Latest events"),
                                                              'project': instance,
                                                              'logs': history[::-1][0:150]})


@require_permission("CREATE", Project)
def add(request):
    return form(request)

@require_permission("EDIT", Project, 'id')
def edit(request, id):
    return form(request, id)


@require_permission("DELETE", Project, "id")
def trash(request, id):
    instance = Project.objects.get(id=id)

    if request.method == "POST":
        if not instance.can_be_deleted()[0]:
            request.message_error("You can't delete this project because: ")
            for reason in instance.can_be_deleted()[1]:
                request.message_error(reason)
        else:
            request.message_success("Successfully deleted this project")
            instance.trash()
        return redirect(overview)
    else:
        return render(request, 'projects/trash.html', {'title': _("Confirm delete"),
                                                                    'project': instance,
                                                                    'can_be_deleted': instance.can_be_deleted()[0],
                                                                    'reasons': instance.can_be_deleted()[1],
                                                                    })


def form (request, id=False):
    if id:
        instance = get_object_or_404(Project, id=id, deleted=False)
        title = _("Edit project")
        msg = "Vellykket endret prosjekt"
        pid = instance.pid
    else:
        instance = Project()
        msg = "Vellykket lagt til nytt prosjekt"
        title = _("New project")
        pid = Project.calculate_next_pid()
        
    #Save and set to active, require valid form
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            request.message_success(msg)

            return redirect(view, o.id)

    else:
        form = ProjectForm(instance=instance, initial={'pid':pid})

    return render(request, "projects/form.html", {'title': title, 'project': instance, 'form': form})
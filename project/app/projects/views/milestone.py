from django.http import HttpResponse
from app.projects.forms import MilestoneForm
from app.projects.models import Project, Milestone
from core.decorators import require_permission
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext as _
from app.projects.views.project import view as viewProject

def add(request, project_id):
    return form(request, project_id)

def edit(request, project_id, milestone_id):
    return form(request, project_id, milestone_id)

def form (request, project_id, milestone_id = False):
    if milestone_id:
        instance = get_object_or_404(Milestone, id=milestone_id, deleted=False)
        title = "Endre prosjekt"
        msg = "Vellykket endret milestone"
    else:
        instance = Milestone()
        msg = "Vellykket lagt til ny milestone"
        title = _("New milestone")

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = MilestoneForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.project = get_object_or_404(Project, id=project_id, deleted=False)
            o.save()
            request.message_success(msg)

            return redirect(viewProject, project_id)

    else:
        form = MilestoneForm(instance=instance)

    return render(request, "form.html", {'title': title, 'form': form})
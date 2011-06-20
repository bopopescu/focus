from django.shortcuts import render, redirect, get_object_or_404
from app.files.forms import FileForm
from app.files.models import File
from app.files.views import generic_form as file_form
from app.projects.models import Project
from core import Core
from core.decorators import require_permission

@require_permission("VIEW", Project, 'id')
def overview(request, id):
    """
    id is project_id
    """
    project = Core.current_user().get_permitted_objects("VIEW", Project).all().get(id=id)

    #Set URL for edit for files in project
    edit_file_url = "/projects/%s/files/" % project.id

    return render(request, "projects/files/list.html",
            {'project': project,
             'file_manager': project,
             'edit_file_url': edit_file_url})


@require_permission("VIEW", Project, 'id')
def add_file(request, id):
    """
    id = project_id
    """
    project = Core.current_user().get_permitted_objects("VIEW", Project).all().get(id=id)
    file = File()
    return file_form(request, project, file, redirect(overview, id))


@require_permission("VIEW", Project, 'id')
def edit_file(request, id, file_id):
    """
    id = project_id
    file_id = file_id
    """
    project = Core.current_user().get_permitted_objects("VIEW", Project).all().get(id=id)
    file = project.files.get(id=file_id)
    return file_form(request, project, file, redirect(overview, id))
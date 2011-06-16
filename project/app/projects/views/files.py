from django.shortcuts import render, redirect, get_object_or_404
from app.files.forms import FileForm
from app.files.models import File
from app.projects.models import Project
from core import Core
from core.decorators import login_required

def overview(request, id):
    """
    id is project_id
    """
    project = Core.current_user().get_permitted_objects("VIEW", Project).all().get(id=id)

    return render(request, "projects/files/list.html", {'project': project})

@login_required()
def add_file(request,id):
    return file_form(request, id)

@login_required()
def edit_file(request, id, file_id):
    return file_form(request, id, file_id)

def file_form (request, id, file_id=None):
    """
    id is project_id
    """

    project_instance = get_object_or_404(Project, id=id, deleted=False)

    if file_id:
        file_instance = get_object_or_404(File, id=file_id, deleted=False)
    else:
        file_instance = File()

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES, instance=file_instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            project_instance.files.add(o)
            
            request.message_success("Successfull")
            return redirect(overview, id)
        
    else:
        form = FileForm(instance=file_instance)

    return render(request, "form.html", {'title': 'Fil',
                                         'form': form,
                                         })
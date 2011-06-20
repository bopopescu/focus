from django.shortcuts import render, redirect, get_object_or_404
from app.files.forms import FileForm
from app.files.models import File
from app.projects.models import Project
from core import Core
from core.decorators import login_required

@login_required()
def add_file(request,id):
    return file_form(request, id)

@login_required()
def edit_file(request, id ):
    return file_form(request, id)

def file_form(request, file_id=None):
    if file_id:
        file_instance = get_object_or_404(File, id=file_id, deleted=False)
    else:
        file_instance = File()

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES, instance=file_instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            request.message_success("Successfully saved")
    else:
        form = FileForm(instance=file_instance)

    return render(request, "form.html", {'title': 'Fil',
                                         'form': form,
                                         })

def generic_form(request, instance, file_instance, redirect_view):
    """
    instance = Project, Product etc
    file_instance = File.objects.get(id=?)
    redirect_view = redirect(overview,id)
    """
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES, instance=file_instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            instance.files.add(o)
            request.message_success("Successfully saved")

            return redirect_view

    else:
        form = FileForm(instance=file_instance)

    return render(request, "files/form.html", {'title': 'Fil',
                                         'form': form,
                                         })
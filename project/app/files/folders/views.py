# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, redirect
from app.files.forms import FolderForm

from app.files.models import File, Folder
from app.files.files.views import overview
from core.decorators import login_required

@login_required()
def add(request, folderID=None):
    return form(request, False, folderID)


@login_required()
def edit(request, id):
    return form(request, id)


@login_required()
def delete(request, id):
    return form(request, id)


@login_required()
def view(request, id):
    file = File.objects.filter().get(id=id)

    who_can_see_this = file.who_has_permission_to('view')
    return render(request, 'files/view.html', {'title': 'Ordre: %s' % file.name,
                                               'file': file,
                                               'who_can_see_this': who_can_see_this})


@login_required()
def form (request, id=False, folderID=None):
    if id:
        instance = get_object_or_404(Folder, id=id, deleted=False)
        msg = "Velykket endret mappe"
    else:
        instance = Folder()
        msg = "Velykket lagt til ny mappe"

    #Set folder, if folderID is set
    folder = None
    if folderID:
        folder = Folder.objects.get(id=folderID)


    #Save and set to active, require valid form
    if request.method == 'POST':
        form = FolderForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user

            if folder:
                o.parent = folder

            o.save()
            form.save_m2m()
            request.message_success(msg)

            return redirect(overview)

    else:
        form = FolderForm(instance=instance)

    return render(request, "form.html", {'title': 'Mappe', 'form': form})

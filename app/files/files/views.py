# -*- coding: utf-8 -*-

from app.files.forms import *
from core.shortcuts import *
from core.views import updateTimeout
from core.decorators import *
from app.files.models import File, Folder

@login_required()
def overview(request):
    folders = Folder.objects.filter(parent=None, creator=Core.current_user())
    print folders
    files = File.objects.filter(folder=None, creator=Core.current_user())

    updateTimeout(request)

    return render_with_request(request, 'files/list.html', {'title': 'Filer',
                                                            'files': files,
                                                            'folders': folders,
                                                            })

def folder(request, folderID):
    folder = Folder.objects.get(id=folderID, creator=Core.current_user())

    folders = Folder.objects.filter(parent=folder, creator=Core.current_user())

    files = File.objects.filter(folder=folder, creator=Core.current_user())

    return render_with_request(request, 'files/list.html', {'title': 'Filer',
                                                            'folder': folder,
                                                            'files': files,
                                                            'folders': folders,
                                                            })

def moveFile(request):
    fileID = request.GET.get("fileID")
    toFolder = request.GET.get("folderID")

    file = File.objects.get(id=fileID)
    file.folder = Folder.objects.get(id=toFolder)
    file.save()

    return

def moveFolder(request):
    folderID = request.GET.get("folderID")
    parentID = request.GET.get("parentID")

    folder = Folder.objects.get(id=folderID)

    if parentID == "root":
        folder.parent = None
        folder.save()
        return

    folder.parent = Folder.objects.get(id=parentID)
    folder.save()

    return


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
    file = File.objects.for_company().get(id=id)

    whoCanSeeThis = file.whoHasPermissionTo('view')
    return render_with_request(request, 'files/view.html', {'title': 'Ordre: %s' % file.name,
                                                            'file': file,
                                                            'whoCanSeeThis': whoCanSeeThis})

"""
@login_required()
def permissions(request, id):
    type = File
    file = type.objects.get(pk=id)

    url = "files/"

    if file.folder:
        url = "files/folder/%s" % file.folder.id

    message = "Vellykket endret tilgang for ordre: %s" % file
    return form_perm(request, type, id, url, message)
"""

@login_required()
def form (request, id=False, folderID=None):
    if id:
        instance = get_object_or_404(File, id=id, deleted=False)
        msg = "Velykket endret fil"
    else:
        instance = File()
        msg = "Velykket lagt til ny fil"


    #Set folder, if folderID is set
    folder = None
    if folderID:
        folder = Folder.objects.get(id=folderID)

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)

            if folder:
                o.folder = folder

            o.save()
            form.save_m2m()

            request.message_success(msg)

            return redirect(overview)


    else:
        form = FileForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Fil',
                                                      'form': form,
                                                      'folder': folder})

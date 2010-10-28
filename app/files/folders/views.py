from app.files.forms import *
from core.shortcuts import *
from core.views import updateTimeout, form_perm
from core.decorators import *
from django.contrib.auth.decorators import login_required
from app.files.models import File, Folder
from app.files.files.views import overview

@login_required
def add(request, folderID = None):
    return form(request, False, folderID)

@login_required
def edit(request, id):
    return form(request, id)

@login_required
def delete(request, id):
    return form(request, id)


@login_required
def view(request, id):
    file = File.objects.for_company().get(id=id)

    whoCanSeeThis = file.whoHasPermissionTo('view')
    return render_with_request(request, 'files/view.html', {'title':'Ordre: %s' % file.name,
                                                             'file':file,
                                                             'whoCanSeeThis':whoCanSeeThis})


"""
@login_required
def permissions(request, id):
    type = Folder
    folder = type.objects.get(pk=id)

    url = "files/"

    if folder.parent:
        url = "files/folder/%s" % folder.parent.id

    message = "Vellykket endret tilgang for mappe: %s" % type.objects.get(pk=id)
    return form_perm(request, type, id, url, message)
"""


@login_required
def form (request, id=False, folderID = None):
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
                o.parent     = folder

            o.save()
            form.save_m2m()
            messages.success(request, msg)

            return redirect(overview)

    else:
        form = FolderForm(instance=instance)

    return render_with_request(request, "form.html", {'title':'Mappe', 'form': form})

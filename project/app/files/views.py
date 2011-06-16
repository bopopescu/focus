from app.files.forms import FileForm
from django.shortcuts import render, redirect, get_object_or_404
from app.files.models import File
from core.decorators import login_required

@login_required()
def file_form (request, id=False, folderID=None):
    if id:
        instance = get_object_or_404(File, id=id, deleted=False)
        msg = "Velykket endret fil"
    else:
        instance = File()
        msg = "Velykket lagt til ny fil"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)

            o.save()

            request.message_success(msg)

            return redirect(overview)


    else:
        form = FileForm(instance=instance)

    return render(request, "form.html", {'title': 'Fil',
                                         'form': form,
                                         })
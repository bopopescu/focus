from django.shortcuts import render, get_object_or_404, redirect
from app.files.forms import FileForm
from app.files.models import File, FileTag
from core.decorators import login_required
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect

@login_required()
def add_file(request, id):
    return file_form(request, id)


@login_required()
def edit_file(request, id ):
    return file_form(request, id)

@login_required()
def recover(request, id ):
    file = File.objects.get(id=id)
    file.recover()

    return HttpResponseRedirect("/")

@login_required()
def delete(request, id):
    file = File.objects.get(id=id)
    file.delete()

    if file.parent_file:
        return edit_file(request, file.parent_file.id)
        
    return HttpResponseRedirect("/")

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


def handle_file_tags(tags):
    """
    Take text-string width tags (tag1,tag2,tag3)
    Returns list of tags
    """

    try:
        tag_objects = []
        for tag in tags.split(","):
            if len(tag) > 1:
                tag = FileTag.objects.get_or_create(name=tag.strip().lower())[0]
                tag_objects.append(tag)
        return tag_objects

    except Exception:
        return []


def generic_form(request, instance, file_instance, redirect_view):
    """
    instance = Project, Product etc
    file_instance = File.objects.get(id=?)
    redirect_view = redirect(overview,id)
    """

    clone = file_instance.clone()

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES, instance=file_instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.parent_file = None
            clone.save()
            o.save()

            o.tags = []
            o.tags.add(*handle_file_tags(request.POST['tags']))
            instance.files.add(o)

            request.message_success("Successfully saved")

            return redirect_view

    else:
        tags = ""
        if file_instance.id:
            for tag in file_instance.tags.all():
                tags += tag.name + ", "

        form = FileForm(instance=file_instance, initial={'tags': tags, 'file': None})

    return render(request, "files/form.html", {'title': _("File form"),
                                               'file': file_instance,
                                               'form': form,
                                               })
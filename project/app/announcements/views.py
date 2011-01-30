# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from core.shortcuts import render_with_request
from core.decorators import *
from forms import *

@login_required()
def overview(request):
    announcements = Announcement.objects.all()
    return render_with_request(request, 'announcements/list.html', {'title': 'Oppslag', 'announcements': announcements})

@login_required()
def overview_deleted(request):
    announcements = Announcement.objects.filter(deleted=True)
    return render_with_request(request, 'announcements/list.html', {'title': 'Oppslag', 'announcements': announcements})

@login_required()
def add(request):
    return form(request)

def view(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    return render_with_request(request, 'announcements/view.html', {'title': 'Oppslag',
                                                                    'announcement': announcement})

def edit(request, id):
    return form(request, id)

def delete(request, id):
    Announcement.objects.filter().get(id=id).delete()
    return redirect(overview)

def recover(request, id):
    Announcement.objects.filter(deleted=True).get(id=id).recover()
    return redirect(overview)

@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(Announcement, id=id, deleted=False)
        msg = "Velykket endret oppslag"
    else:
        instance = Announcement()
        msg = "Velykket lagt til ny oppslag"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            request.message_success(msg)
            return redirect(view, o.id)

    else:
        form = AnnouncementForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Oppslag', 'form': form})
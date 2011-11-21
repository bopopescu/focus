# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from app.announcements.forms import AnnouncementForm
from app.announcements.models import Announcement
from core import Core
from core.decorators import login_required
from app.dashboard.views import overview

@login_required()
def overview_trashed(request):
    announcements = Core.current_user().get_permitted_objects("VIEW", Announcement).filter(trashed=True)
    return render(request, 'announcements/list.html', {'title': 'Oppslag', 'announcements': announcements})

@login_required()
def add(request):
    return form(request)

@login_required()
def view(request, id):
    announcement = Core.current_user().get_permitted_objects("VIEW", Announcement).get(id=id)
    return render(request, 'announcements/view.html', {'title': 'Oppslag',
                                                                    'announcement': announcement})

@login_required()
def edit(request, id):
    return form(request, id)

@login_required()
def trash(request, id):
    Announcement.objects.filter().get(id=id).delete()
    return redirect(overview)

@login_required()
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
            return redirect(overview)

    else:
        form = AnnouncementForm(instance=instance, initial={"attachment":None})

    return render(request, "announcements/form.html", {'title': 'Oppslag', 'announcement':instance, 'form': form})
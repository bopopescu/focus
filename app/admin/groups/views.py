# -*- coding: utf-8 -*-
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from app.admin.forms import *
from core.decorators import login_required
from core.models import Group
from core.shortcuts import *
from core.views import updateTimeout

@login_required()
def overview(request):
    updateTimeout(request)
    groups = Group.objects.inCompany()
    return render_with_request(request, 'admin/groups/list.html', {'title': 'Grupper', 'groups': groups})

def add(request):
    return form(request)

@login_required()
def edit(request, id):
    return form(request, id)

@login_required()
def addPop(request):
    instance = User()

    if request.method == "POST":
        form = GroupForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()

            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                    ((o._get_pk_val()), (o)))

    else:
        form = GroupForm(instance=instance)

    return render_with_request(request, "simpleform.html", {'title': 'Bruker', 'form': form})


@login_required()
def view(request, id):

    group = Group.objects.get(id=id)
    
    return render_with_request(request, 'admin/groups/view.html', {'title': 'Gruppe',
                                                                        'group': group,
                                                                        })

@login_required()
def delete(request, id):
    request.messages_success("Velykket slettet bruker")
    return redirect(overview)

@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(Group, id=id)
        msg = "Velykket endret gruppe"
    else:
        instance = Group()
        msg = "Velykket lagt til ny gruppe"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.company = Core.current_user().get_company()
            o.save()
            form.save_m2m()

            request.message_success(msg)
            return redirect(overview)

    else:
        form = GroupForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Gruppe', 'form': form})
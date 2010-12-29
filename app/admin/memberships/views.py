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
    Memberships = Group.objects.for_company()
    return render_with_request(request, 'admin/memberships/list.html', {'title': 'Grupper', 'memberships': Memberships})

def add(request):
    return form(request)

@login_required()
def edit(request, id):
    return form(request, id)

def get_permissions(membership):
    """Permissions = ObjectPermission.objects.filter(
            (

            Q(membership=membership)

            )
            ).order_by('content_type')
    return Permissions
    """
    pass

@login_required()
def addPop(request):
    instance = User()

    if request.method == "POST":
        form = MembershipForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()

            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                    ((o._get_pk_val()), (o)))

    else:
        form = MembershipForm(instance=instance)

    return render_with_request(request, "simpleform.html", {'title': 'Bruker', 'form': form})


@login_required()
def view(request, id):
    membership = Membership.objects.get(id=id)

    Permissions = get_permissions(membership)

    return render_with_request(request, 'admin/memberships/view.html', {'title': 'Gruppe',
                                                                        'membership': membership,
                                                                        'permissions': Permissions,
                                                                        })

@login_required()
def delete(request, id):
    request.messages_success("Velykket slettet bruker")
    return redirect(overview)

@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(Membership, id=id)
        msg = "Velykket endret gruppe"
    else:
        instance = Membership()
        msg = "Velykket lagt til ny gruppe"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = MembershipForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            form.save_m2m()

            request.messages_success(msg)
            #Redirects after save for direct editing
            return redirect(overview)


    else:
        form = MembershipForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Gruppe', 'form': form})
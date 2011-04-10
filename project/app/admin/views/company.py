# -*- coding: utf-8 -*-

from core import Core
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from app.company.forms import CompanyForm
from core.auth.company.models import Company
from core.decorators import require_permission

@require_permission("CONFIGURE", Company)
def editCompany(request):
    id = Core.current_user().get_company().id

    instance = get_object_or_404(Company, id=id)
    msg = _("Successfully edited your company")

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            form.save_m2m()

            request.message_success(msg)

            #Redirects after save for direct editing
            return redirect(editCompany)

    else:
        form = CompanyForm(instance=instance)

    return render(request, "form.html", {'title': _('Company details'), 'form': form})
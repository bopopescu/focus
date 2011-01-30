# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from core.shortcuts import *
from core.decorators import *
from app.company.forms import *

@require_permission("CONFIGURE", Company)
def editCompany(request):
    id = Core.current_user().get_company().id

    instance = get_object_or_404(Company, id=id)
    msg = "Velykket endret ditt firma"

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

    return render_with_request(request, "form.html", {'title': 'Firmadetaljer', 'form': form})
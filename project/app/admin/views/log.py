from django.shortcuts import render
from core import Core
from core.auth.log.models import Log
from django.utils.translation import ugettext as _
from core.decorators import login_required

@login_required()
def overview(request):
    logs = Log.objects.filter(company=Core.current_user().get_company()).order_by('id').reverse()[:150]
    return render(request, 'admin/log.html', {'title': _("Log"), 'logs': logs})
from django.contrib.auth.decorators import login_required, permission_required
from core.shortcuts import *
from core.decorators import *
from app.announcements.models import * 
from core.views import updateTimeout


@login_required
def overview(request):
    
    
    updateTimeout(request)
    announcements = Announcement.objects.for_user()[::-1]
    your_projects = Project.objects.for_user()
    your_orders = Order.objects.for_user()[::-1]
        
    return render_with_request(request, 'dashboard/dashboard.html', {'title':'Oppslagstavle',
                                                                     'announcements':announcements,
                                                                     'orders':your_orders,
                                                                     'projects':your_projects})
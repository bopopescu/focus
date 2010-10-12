from django.contrib.auth.decorators import login_required
from core.shortcuts import *
from app.announcements.models import *
from core.views import updateTimeout
from app.orders.models import Order
from app.projects.models import Project, Project


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
from django.contrib.auth.decorators import login_required
from core.shortcuts import *
from app.announcements.models import *
from core.views import updateTimeout
from app.orders.models import Order
from app.projects.models import Project, Project
from core.models import Log, Notification
from core.middleware import get_current_company, get_current_user


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

def logs(request):

    logs = Log.objects.filter(company=get_current_company())
    return render_with_request(request, 'dashboard/listLog.html', {'title':'Siste 30 hendelser',
                                                                   'logs': logs[1:30][::-1]} )


def notifications(request):

    #Get all notifactions
    notifications = Notification.objects.filter(recipient=get_current_user(), read=False)

    newNotifications = []

    for i in notifications:
        newNotifications.append(i)

    #Set to read, so they wont bother the user anymore.
    Notification.objects.filter(recipient=get_current_user()).update(read=True)

    return render_with_request(request, 'dashboard/notifications.html', {'title':'Siste 30 hendelser',
                                                                         'notifications': newNotifications} )
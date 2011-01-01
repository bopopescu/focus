# -*- coding: utf-8 -*-

from app.announcements.models import Announcement
from app.orders.models import Order
from app.projects.models import Project
from core import Core
from core.decorators import login_required
from core.models import Log, Notification
from core.shortcuts import render_with_request

@login_required()
def overview(request):
    announcements = Announcement.objects.all()[::-1]
    your_projects = Project.objects.all()
    your_orders = Order.objects.all().filter(state="O")[::-1]

    return render_with_request(request, 'dashboard/dashboard.html', {'title': 'Oppslagstavle',
                                                                     'announcements': announcements,
                                                                     'orders': your_orders,
                                                                     'projects': your_projects})

@login_required()
def logs(request):
    #logs = Log.objects.filter(company=get_current_company())
    logs = Log.objects.all()
    return render_with_request(request, 'dashboard/listLog.html', {'title': 'Siste hendelser',
                                                                   'logs': logs[::-1][0:150]})

@login_required()
def notifications(request):
    #Get all notifactions
    notifications = Notification.objects.filter(recipient=Core.current_user(), read=False)
    oldNotificationsS = Notification.objects.filter(recipient=Core.current_user(), read=True)

    newNotifications = []
    oldNotifications = []

    for i in notifications:
        newNotifications.append(i)

    for i in oldNotificationsS:
        oldNotifications.append(i)

    #Set to read, so they wont bother the user anymore.
    Notification.objects.filter(recipient=Core.current_user()).update(read=True)

    return render_with_request(request, 'dashboard/notifications.html', {'title': 'Oppdateringer',
                                                                         'notifications': newNotifications,
                                                                         'oldNotifications': oldNotifications[::-1][
                                                                                             0:150]})
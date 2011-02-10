# -*- coding: utf-8 -*-

from app.announcements.models import Announcement
from app.orders.models import Order
from app.projects.models import Project
from core import Core
from core.decorators import login_required
from core.models import Log, Notification
from core.shortcuts import render_with_request
from django.utils.translation import ugettext as _

@login_required()
def overview(request):
    title = _("Welcome to TIME")

    announcements = Core.current_user().getPermittedObjects("VIEW", Announcement)[::-1]
    your_projects = Core.current_user().getPermittedObjects("VIEW", Project)

    your_orders = Core.current_user().getPermittedObjects("VIEW", Order).filter(state="Order")[::-1]

    return render_with_request(request, 'dashboard/dashboard.html', {'title': title,
                                                                     'announcements': announcements,
                                                                     'orders': your_orders,
                                                                     'projects': your_projects})

@login_required()
def logs(request):
    #logs = Log.objects.filter(company=get_current_company())
    logs = Log.objects.all()
    return render_with_request(request, 'dashboard/listLog.html', {'title': _("Latest events"),
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

    return render_with_request(request, 'dashboard/notifications.html', {'title': _('Updates'),
                                                                         'notifications': newNotifications,
                                                                         'oldNotifications': oldNotifications[::-1][
                                                                                             0:150]})

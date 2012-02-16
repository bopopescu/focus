# -*- coding: utf-8 -*-
from app.tickets.models import Ticket
from core import Core
from app.announcements.models import Announcement
from app.orders.models import Order
from app.projects.models import Project
from core.decorators import login_required, require_permission
from core.models import  Notification
from django.shortcuts import render
from django.utils.translation import ugettext as _

@require_permission("LIST", Announcement)
def overview(request):
    title = _("Welcome to TIME")

    announcements = Core.current_user().get_permitted_objects("VIEW", Announcement)[::-1]
    #your_projects = Core.current_user().get_permitted_objects("VIEW", Project, order_by="?")[0:3]
    #your_orders = Core.current_user().get_permitted_objects("VIEW", Order, order_by="?")[0:3]
    #tickets = Core.current_user().get_permitted_objects("VIEW", Ticket, order_by="?")[0:3]



    return render(request, 'dashboard/dashboard.html', {'title': title,
                                                        'announcements': announcements,
                                                        })


@login_required()
def notifications(request):
    #Get all notifactions
    notifications = Notification.objects.filter(recipient=Core.current_user(), read=False).order_by("id").reverse()
    oldNotificationsS = Notification.objects.filter(recipient=Core.current_user(), read=True).order_by("id").reverse()[
                        0:10]

    newNotifications = []
    oldNotifications = []

    for i in notifications:
        newNotifications.append(i)

    for i in oldNotificationsS:
        oldNotifications.append(i)

    #Set to read, so they wont bother the user anymore.
    Notification.objects.filter(recipient=Core.current_user()).update(read=True)

    return render(request, 'dashboard/notifications.html', {'title': _('Updates'),
                                                            'notifications': newNotifications,
                                                            'oldNotifications': oldNotifications})
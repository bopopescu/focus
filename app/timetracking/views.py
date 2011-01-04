# -*- coding: utf-8 -*-
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from app.timetracking.helpers import calculateHoursWorked
from core.decorators import require_permission, login_required
from forms import *
from core.shortcuts import *
from django.contrib import messages
from django.utils.html import escape
from core.views import updateTimeout
from datetime import date, datetime
import time
from calendar import monthrange

@require_permission("LIST", Timetracking)
def overview(request):
    updateTimeout(request)

    return listTimetrackings(request, Core.current_user(), generateValidPeriode()[0], generateValidPeriode()[1])

def viewArchivedMonth(request, year, month, user_id=None):
    updateTimeout(request)

    year = int(year)
    month = int(month)

    daysInMonth = monthrange(year, month)[1]

    from_date = date(year, month, 1)
    to_date = date(year, month, daysInMonth)

    user = Core.current_user()

    if user_id:
        user = User.objects.get(id=user_id)

    return listTimetrackings(request, user, from_date.strftime("%d.%m.%Y"), to_date.strftime("%d.%m.%Y"))

def listTimetrackings(request, user, from_date, to_date):

    timetrackings = user.getPermittedObjects("VIEW", Timetracking).filter(creator=user)

    unwanted = []

    from_date = time.mktime(time.strptime("%s" % (from_date), "%d.%m.%Y"))
    to_date = time.mktime(time.strptime("%s" % (to_date), "%d.%m.%Y"))

    for obj in timetrackings:
        date = time.mktime(time.strptime(obj.date.strftime("%d.%m.%Y"), "%d.%m.%Y"))
        if not (date >= from_date and date <= to_date):
            unwanted.append(obj.id)

    timetrackings = timetrackings.exclude(id__in=unwanted)

    sumHours = 0
    sumEarned = 0
    sumCover = 0
    sumTotalEarned = 0
    
    for t in timetrackings:
        if t.hours_worked:
            sumHours += Decimal(t.hours_worked)
        if t.hours_worked and t.hourly_rate:
            sumEarned += Decimal(t.hours_worked) * Decimal(t.hourly_rate)
        
    sumTotalEarned = sumEarned

    if user.percent_cover:
        a = Decimal(user.percent_cover)/100
        sumCover = a * Decimal(sumEarned)
        sumTotalEarned = sumEarned-sumCover

    return render_with_request(request, 'timetracking/list.html',
                               {'title': 'Timeføringer', 'timetrackings': timetrackings,
                                'sumHours': round(sumHours,2),
                                'sumEarned': round(sumEarned,2),
                                'sumCover': round(sumCover,2),
                                'sumTotalEarned': round(sumTotalEarned,2)})

def your_archive(request):
    return archive(request)

def user_archive(request,user_id):
    return archive(request, user_id)

def archive(request, user_id=None):
    updateTimeout(request)

    year_with_months = {}

    user = Core.current_user()
    
    if user_id:
        user = User.objects.get(id=user_id)
        
    timetrackings = user.getPermittedObjects("VIEW", Timetracking).filter(creator=user)

    for time in timetrackings:
        year_with_months[time.date.year] = set([])

    for time in timetrackings:
        year_with_months[time.date.year].add(time.date.month)

    return render_with_request(request, 'timetracking/archive.html',
                               {'title': 'Arkiv', 'year_with_months': year_with_months})


@require_permission("CREATE", Timetracking)
def add(request):
    return form(request)


@require_permission("EDIT", Timetracking, "id")
def edit(request, id):
    #Check if valid for edit

    time = get_object_or_404(Timetracking, id=id, deleted=False)

    if validForEdit(time.date.strftime("%d.%m.%Y")):
        return form(request, id)

    request.message_error("Du kan ikke redigere denne timen")
    return redirect(overview)


@require_permission("DELETE", Timetracking, "id")
def delete(request, id):
    Timetracking.objects.get(id=id).delete()
    return redirect(overview)

def addAjax(request):
    return

@require_permission("CREATE", Timetracking)
def addTypeOfWork(request):
    instance = TypeOfTimeTracking()
    msg = "Velykket lagt til ny type arbeid"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = TypeOfTimeTrackingForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            request.message_success(request, msg)

            #Redirects after save for direct editing
            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                    (escape(o._get_pk_val()), escape(o)))
    else:
        form = TypeOfTimeTrackingForm(instance=instance)

    return render_with_request(request, "simpleform.html", {'title': 'Typer arbeid', 'form': form})

@require_permission("LIST", Timetracking)
def calendar(request):
    timetrackings = Timetracking.objects.all()

    instance = Timetracking()
    form = TimetrackingForm(request.POST, instance=instance)

    return render_with_request(request, "timetracking/calendar.html", {'title': 'Timeregistrering',
                                                                       'timetrackings': timetrackings,
                                                                       'form': form, })

@login_required()
def ajaxEditCalendar(request):
    from django.utils import simplejson

    timeTrackingID = request.GET.get("timeTrackingID")

    if timeTrackingID:
        t = Timetracking.objects.get(id=timeTrackingID)
    else:
        t = Timetracking()

    o = Order.objects.get(id=1)
    b = TypeOfTimeTracking.objects.get(id=1)

    time_start = "%s" % request.GET.get("time_start")
    time_stop = "%s" % request.GET.get("time_end")

    datAe = request.GET.get("date")
    tempDate = time.strptime(datAe, "%d.%m.%Y")
    k = date(tempDate[0], tempDate[1], tempDate[2])

    t.hours_worked = 1
    t.typeOfWork = b
    t.order = o
    t.date = k
    t.time_start = time_start
    t.time_end = time_stop

    t.save()

    data = simplejson.dumps({'id': t.id})

    return HttpResponse(data)


@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(Timetracking, id=id, deleted=False)
        msg = "Velykket endret timeføring"
    else:
        instance = Timetracking()
        msg = "Velykket lagt til nytt timeføring"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = TimetrackingForm(request.POST, instance=instance)

        if form.is_valid():
            date = request.POST['date']

            start = time.strptime("%s %s" % (date, request.POST['time_start']), "%d.%m.%Y  %H:%M")
            end = time.strptime("%s %s" % (date, request.POST['time_end']), "%d.%m.%Y  %H:%M")

            start_t = time.mktime(start)
            end_t = time.mktime(end)

            clockValid = True

            if start_t > end_t:
                request.message_error("Du kan ikke slutte før du begynte")
                clockValid = False

            hoursWorked = calculateHoursWorked(request, start_t, end_t)

            if hoursWorked <= 0:
                clockValid = False

            if clockValid:
                o = form.save(commit=False)
                o.hours_worked = hoursWorked
                o.save()
                request.message_success(msg)

                #Redirects after save for direct editing
                return overview(request)


    else:
        form = TimetrackingForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Timeføring', 'form': form})
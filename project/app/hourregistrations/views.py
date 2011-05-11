# -*- coding: utf-8 -*-
from decimal import Decimal
from django.shortcuts import render
from app.hourregistrations.forms import HourRegistrationForm
from app.hourregistrations.models import HourRegistration
from core import Core
from core.auth.user.models import User
from core.decorators import login_required
from datetime import datetime, date
from django.utils import simplejson
from django.utils.simplejson import JSONEncoder
from django.http import HttpResponse
import calendar
import time

@login_required()
def form(request):
    id = int(request.POST['id'])

    instance = HourRegistration()

    if id:
        instance = HourRegistration.objects.get(id=id)

    form = HourRegistrationForm(request.POST, instance=instance)

    if form.is_valid():
        a = form.save(commit=False)
        a.date = datetime.strptime(request.POST['date'], "%Y-%m-%d")
        a.save()

        return HttpResponse(simplejson.dumps({'name': str(a.date),
                                              'id': a.id,
                                              'valid': True}), mimetype='application/json')
    else:
        errors = dict([(field, errors[0]) for field, errors in form.errors.items()])

        return HttpResponse(simplejson.dumps({'errors': errors,
                                              'valid': False}), mimetype='application/json')

    return HttpResponse("ERROR")


@login_required()
def list_all_employees(request):
    persons = User.objects.filter_current_company()

    return render(request, 'hourregistrations/list_persons.html', {'persons': persons})


@login_required()
def calendar_day_json(request, year, month, day):
    date = datetime.strptime("%s-%s-%s" % (year, month, day), "%Y-%m-%d")

    list_hour_registrations = HourRegistration.objects.filter(date=date, creator=Core.current_user())

    registrations = [{'id': reg.id,
                      'time_start': reg.time_start,
                      'time_end': reg.time_end,
                      'hours_worked': str(reg.hours_worked),
                      'order': reg.order.id,
                      'pause': str(reg.pause),
                      'customer_name': reg.order.customer.full_name,
                      'order_name': reg.order.title,
                      'description': reg.description
                     } for reg in list_hour_registrations]

    return HttpResponse(JSONEncoder().encode(registrations), mimetype='application/json')


@login_required()
def calendar_json(request, year, month):
    year = int(year)
    month = int(month)

    date = datetime.strptime("%s-%s-%s" % (year, month, 1), "%Y-%m-%d")

    NOW = datetime.now()
    CURRENT_WEEK = date.isocalendar()[1]

    cal_month = calendar.monthcalendar(year, month)
    temp_cal = []

    #Build
    for week in cal_month:
        hours_count = 0
        for day in week:
            if int(day) > 0:
                day_date = datetime.strptime("%s-%s-%s" % (year, month, int(day)), "%Y-%m-%d")

                for reg in HourRegistration.objects.filter(date=day_date, creator=Core.current_user()):
                    hours_count += float(reg.hours_worked)

            if NOW == date:
                temp_cal.append((CURRENT_WEEK, day, "day today", hours_count))
            elif(day > 0):
                temp_cal.append((CURRENT_WEEK, day, "day", hours_count))
            else:
                temp_cal.append((CURRENT_WEEK, day, "", hours_count))

            hours_count = 0

        if CURRENT_WEEK == 52:
            CURRENT_WEEK = 0
        CURRENT_WEEK += 1

    return HttpResponse(JSONEncoder().encode(temp_cal), mimetype='application/json')


@login_required()
def date_valid_for_edit(request, year, month, day):
    response = Core.current_user().can_edit_hour_date("%s.%s.%s" % (day, month, year))
    return HttpResponse(JSONEncoder().encode(response), mimetype='application/json')


@login_required()
def calendar_today(request):
    form = HourRegistrationForm()
    return render(request, "hourregistrations/calendar.html", {"form": form})


@login_required()
def calendar_can_edit_form(request):
    reg = HourRegistration.objects.get()
    print Core.current_user()

########ARCHIVE#############

def view_archived_month(request, year, month, user_id=None):
    year = int(year)
    month = int(month)

    daysInMonth = calendar.monthrange(year, month)[1]

    from_date = date(year, month, 1)
    to_date = date(year, month, daysInMonth)

    user = Core.current_user()

    if user_id:
        user = User.objects.get(id=user_id)

    return list_hour_registrations(request, user, from_date.strftime("%d.%m.%Y"), to_date.strftime("%d.%m.%Y"))


def list_hour_registrations(request, user, from_date, to_date):
    HourRegistrations = user.get_permitted_objects("VIEW", HourRegistration).filter(creator=user)

    unwanted = []

    from_date = time.mktime(time.strptime("%s" % (from_date), "%d.%m.%Y"))
    to_date = time.mktime(time.strptime("%s" % (to_date), "%d.%m.%Y"))

    for obj in HourRegistrations:
        date = time.mktime(time.strptime(obj.date.strftime("%d.%m.%Y"), "%d.%m.%Y"))
        if not (date >= from_date and date <= to_date):
            unwanted.append(obj.id)

    HourRegistrations = HourRegistrations.exclude(id__in=unwanted)

    sumHours = 0
    sumEarned = 0
    sumCover = 0
    sumTotalEarned = 0
    sumKilometers = 0
    sumDisbursements = 0

    for t in HourRegistrations:
        if t.hours_worked:
            sumHours += Decimal(t.hours_worked)
        if t.hours_worked and t.hourly_rate:
            sumEarned += Decimal(t.hours_worked) * Decimal(t.hourly_rate)
        if t.disbursements:
            for disb in t.disbursements.all():
                sumDisbursements += disb.price
        if t.drivingregistration:
            for driving in t.drivingregistration.all():
                sumKilometers += driving.kilometres

    sumTotalEarned = sumEarned

    if user.percent_cover:
        a = Decimal(user.percent_cover) / 100
        sumCover = a * Decimal(sumEarned)
        sumTotalEarned = sumEarned - sumCover

    return render(request, 'hourregistrations/list_hours.html',
                  {'title': 'Timeføringer', 'hourregistrations': HourRegistrations,
                   'sumHours': round(sumHours, 2),
                   'sumEarned': round(sumEarned, 2),
                   'sumCover': round(sumCover, 2),
                   'sumTotalEarned': round(sumTotalEarned, 2),
                   'sumDisbursements': round(sumDisbursements, 2),
                   'sumKilometers': round(sumKilometers, 2)})


def your_archive(request):
    return archive(request)


def user_archive(request, user_id):
    return archive(request, user_id)


def archive(request, user_id=None):
    year_with_months = {}

    user = Core.current_user()

    if user_id:
        user = User.objects.get(id=user_id)

    HourRegistrations = user.get_permitted_objects("VIEW", HourRegistration).filter(creator=user)

    for time in HourRegistrations:
        year_with_months[time.date.year] = set([])

    for time in HourRegistrations:
        year_with_months[time.date.year].add(time.date.month)

    return render(request, 'hourregistrations/archive.html',
                  {'title': 'Arkiv', 'year_with_months': year_with_months})

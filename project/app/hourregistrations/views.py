# -*- coding: utf-8 -*-
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from api.hourregistrationsapi.forms import TimeTrackerForm
from app.hourregistrations.forms import HourRegistrationForm, HourRegistrationTypeForm, DisbursementForm
from app.hourregistrations.models import HourRegistration, HourRegistrationType, Disbursement
from core import Core
from core.auth.user.models import User
from core.decorators import login_required, require_permission
from datetime import datetime, date
from django.utils import simplejson
from django.utils.simplejson import JSONEncoder
from django.http import HttpResponse
from django.utils.translation import ugettext as _
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
                                              'valid': True}), mimetype='application/json')

    else:
        errors = dict([(field, errors[0]) for field, errors in form.errors.items()])

        return HttpResponse(simplejson.dumps({'errors': errors,
                                              'valid': False}), mimetype='application/json')

    return HttpResponse("ERROR")


@login_required()
def delete(request, id):
    if id:
        instance = HourRegistration.objects.get(id=id)
        instance.delete()
        return HttpResponse("OK")
    else:
        return HttpResponse("ERROR")


@require_permission("CONFIGURE", HourRegistration)
def list_all_employees(request):
    persons = User.objects.filter_current_company()

    return render(request, 'hourregistrations/list_persons.html', {'persons': persons})


@require_permission("LIST", HourRegistration)
def calendar_day_json(request, year, month, day):
    date = datetime.strptime("%s-%s-%s" % (year, month, day), "%Y-%m-%d")

    list_hour_registrations = HourRegistration.objects.filter(date=date, creator=Core.current_user())

    registrations = [{'id': reg.id,
                      'time_start': reg.time_start,
                      'time_end': reg.time_end,
                      'hours': str(reg.hours),
                      'order': reg.order.id,
                      'type': str(reg.type.id),
                      'customer_name': reg.get_customer_name(),
                      'order_name': reg.get_order_name(),
                      'description': reg.description
    } for reg in list_hour_registrations]

    return HttpResponse(JSONEncoder().encode(registrations), mimetype='application/json')


@require_permission("LIST", HourRegistration)
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
                    hours_count += float(reg.hours)

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


@require_permission("LIST", HourRegistration)
def date_valid_for_edit(request, year, month, day):
    response = Core.current_user().can_edit_hour_date("%s.%s.%s" % (day, month, year))
    return HttpResponse(JSONEncoder().encode(response), mimetype='application/json')


@require_permission("LIST", HourRegistration)
def calendar_today(request):
    form = HourRegistrationForm()
    return render(request, "hourregistrations/calendar.html", {"form": form})


def timer(request):
    form = TimeTrackerForm()
    return render(request, 'hourregistrations/timer.html', {'form': form})


@require_permission("LIST", HourRegistration)
def calendar_can_edit_form(request):
    reg = HourRegistration.objects.get()
    print Core.current_user()


@require_permission("EDIT", HourRegistrationType)
def admin_hourregistrationtypes(request, id=None):
    instance = HourRegistrationType()
    types = HourRegistrationType.objects.filter(trashed=False, company = Core.current_user().get_company())

    if id:
        instance = get_object_or_404(HourRegistrationType, id=id)

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = HourRegistrationTypeForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.save()

            request.message_success("Success")

            return redirect(admin_hourregistrationtypes, o.id)
    else:
        form = HourRegistrationTypeForm(instance=instance)

    return render(request, "hourregistrations/types.html",
            {'title': _("Hour registrations types"), 'types': types, 'form': form})


@require_permission("EDIT", Disbursement)
def disbursements(request, id=None):
    instance = Disbursement()
    disb = Disbursement.objects.filter(trashed=False, creator=Core.current_user())

    if id:
        instance = get_object_or_404(Disbursement, id=id)

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = DisbursementForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.save()

            request.message_success("Success")

            return redirect(disbursements)

    else:
        form = DisbursementForm(instance=instance, initial={'attachment': None})

    return render(request, "hourregistrations/disbursements.html",
            {'title': _("Disbursements"), 'disbursements': disb, 'disbursement': instance, 'form': form})

########ARCHIVE#############

@require_permission("MANAGE", HourRegistration)
def view_archived_month(request, year, month, user_id=None, print_friendly=False):
    year = int(year)
    month = int(month)

    daysInMonth = calendar.monthrange(year, month)[1]

    from_date = date(year, month, 1)
    to_date = date(year, month, daysInMonth)

    user = Core.current_user()

    if user_id:
        user = User.objects.get(id=user_id)

    template = "hourregistrations/list_hours.html"

    if print_friendly:
        template = "hourregistrations/list_hours_print_friendly.html"

    return list_hour_registrations(request, user, from_date, to_date, template)


@require_permission("MANAGE", HourRegistration)
def list_hour_registrations(request, user, from_date, to_date, template):
    hourregistrations = HourRegistration.objects.filter(creator=user,
                                                        date__gte=from_date,
                                                        date__lte=to_date)

    sumHours = 0
    sumEarned = 0
    sumCover = 0

    sum_totals = {}

    for t in hourregistrations:
        if t.hours:

            if not sum_totals.has_key('%s' % t.type.name):
                sum_totals['%s' % t.type.name] = 0.0

            sum_totals['%s' % t.type.name] += 3
            sumHours += Decimal(t.hours)

        if t.hours and t.hourly_rate:
            sumEarned += Decimal(t.hours) * Decimal(t.hourly_rate)

    sumTotalEarned = sumEarned

    if user.percent_cover:
        a = Decimal(user.percent_cover) / 100
        sumCover = a * Decimal(sumEarned)
        sumTotalEarned = sumEarned - sumCover

    return render(request, template,
            {'title': 'Timeføringer %s' % (user), 'hourregistrations': hourregistrations,
             'sumHours': round(sumHours, 2),
             'sumEarned': round(sumEarned, 2),
             'sumCover': round(sumCover, 2),
             'sum_totals':sum_totals,
             'sumTotalEarned': round(sumTotalEarned, 2)})


@require_permission("LIST", HourRegistration)
def your_archive(request):
    return archive(request)


@require_permission("MANAGE", HourRegistration)
def user_archive(request, user_id):
    return archive(request, user_id)


def archive(request, user_id=None):
    year_with_months = {}

    user = Core.current_user()

    if user_id:
        user = User.objects.get(id=user_id)

    HourRegistrations = HourRegistration.objects.filter(creator=user)

    for time in HourRegistrations:
        year_with_months[time.date.year] = set([])

    for time in HourRegistrations:
        year_with_months[time.date.year].add(time.date.month)

    return render(request, 'hourregistrations/archive.html',
            {'title': 'Arkiv',
             'user_id': user.id,
             'year_with_months': year_with_months})
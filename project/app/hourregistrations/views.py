from django.shortcuts import render
from app.hourregistrations.forms import HourRegistrationForm
from app.hourregistrations.models import HourRegistration
from app.orders.models import Order
from core import Core
from core.decorators import login_required
from datetime import datetime
from django.utils import simplejson
from django.utils.simplejson import JSONEncoder
from django.http import HttpResponse
import calendar

@login_required()
def form(request):

    id = int(request.POST['id'])

    instance = HourRegistration()

    if id:
        instance = HourRegistration.objects.get(id=id)

    form = HourRegistrationForm(request.POST, instance=instance)

    if form.is_valid():
        a = form.save(commit=False)
        a.date = datetime.strptime(request.POST['date'],"%Y-%m-%d")
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
def calendar_day_json(request, year, month, day):
    date = datetime.strptime("%s-%s-%s" % (year, month, day), "%Y-%m-%d")

    listHourRegistrations = HourRegistration.objects.filter(date=date, creator=Core.current_user())

    registrations = [{'id': reg.id,
                      'time_start': reg.time_start,
                      'time_end': reg.time_end,
                      'order': reg.order.id,
                      'pause': str(reg.pause),
                      'customer_name': reg.order.customer.full_name,
                      'order_name': reg.order.order_name,
                      'description': reg.description
                     } for reg in listHourRegistrations]

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
    response = Core.current_user().can_edit_hour_date("%s.%s.%s"%(day,month,year))
    return HttpResponse(JSONEncoder().encode(response), mimetype='application/json')

@login_required()
def calendar_today(request):
    form = HourRegistrationForm()

    return render(request, "hourregistrations/calendar.html", {"form":form})

@login_required()
def calendar_can_edit_form(request):
    reg = HourRegistration.objects.get()
    print Core.current_user()
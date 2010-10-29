# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from models import *
from forms import *
from core.shortcuts import *
from django.contrib import messages
from django.utils.html import escape 
from core.views import updateTimeout
import time

@login_required
def overview(request):
    updateTimeout(request)
    timetrackings = Timetracking.objects.for_user()    
    return render_with_request(request, 'timetracking/list.html', {'title':'Timeføringer', 'timetrackings':timetrackings})

@login_required
def add(request):
    return form(request)


@login_required
def edit(request, id):
    return form(request, id)


@login_required
def delete(request, id):
    Timetracking.objects.get(id=id).delete()
    return redirect(overview)

def addAjax(request):
    return

@login_required
def addTypeOfWork(request):
    instance = TypeOfTimeTracking()
    msg = "Velykket lagt til ny type arbeid"
            
    #Save and set to active, require valid form
    if request.method == 'POST':
        form = TypeOfTimeTrackingForm(request.POST, instance=instance)       
        if form.is_valid():    
            o = form.save(commit=False)
            o.save()
            messages.success(request, msg)        

            #Redirects after save for direct editing
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                           (escape(o._get_pk_val()), escape(o)))            
    else:
        form = TypeOfTimeTrackingForm(instance=instance)
    
    return render_with_request(request, "simpleform.html", {'title':'Typer arbeid', 'form': form })



@login_required
def calculateHoursWorked(request, start, end):


    diff = 0
    start = time.strptime("2010 " + start, "%Y %H:%M")
    end = time.strptime("2010 " + end, "%Y %H:%M")
    diff = time.mktime(end)-time.mktime(start)

    if diff<1:
        mg = "Sjekk klokkeslettene en gang til"
        messages.error(request, mg)

    diff = str(diff/3600)


    return diff



@login_required
def calendar(request):
    timetrackings = Timetracking.objects.for_user()

    return render_with_request(request, "timetracking/calendar.html", {'title':'Timeregistrering','timetrackings':timetrackings })


@login_required
def ajaxResizeCalendar(request):

    timeTrackingID          = request.GET.get("timeTrackingID")

    TimeTracking            = Timetracking.objects.get(id=timeTrackingID)

    time_start = "%s" % request.GET.get("time_start")
    time_stop = "%s" % request.GET.get("time_end")

    TimeTracking.time_start = time_start
    TimeTracking.time_end   = time_stop

    TimeTracking.save()
    return HttpResponse("OK")

@login_required
def ajaxAddCalendar(request):

    Timetracking(hours_worked=1).save()

    return HttpResponse("OK")

@login_required
def form (request, id = False):
        
    if id:
        instance = get_object_or_404(Timetracking, id = id, deleted=False)
        msg = "Velykket endret timeføring"
    else:
        instance = Timetracking()
        msg = "Velykket lagt til nytt timeføring"
            
    #Save and set to active, require valid form
    if request.method == 'POST':
    
    
        form = TimetrackingForm(request.POST, instance=instance)       
        
        clockValid = True
        hoursWorked = calculateHoursWorked(request, request.POST['time_start'], request.POST['time_end']) == 0
        if hoursWorked == 0:
            clockValid = False
            
        if form.is_valid() and clockValid:    
            o = form.save(commit=False)
            o.hours_worked = hoursWorked
            o.save()
            messages.success(request, msg)        

            #Redirects after save for direct editing
            return overview(request)  
        
        
    else:
        form = TimetrackingForm(instance=instance)
    
    return render_with_request(request, "form.html", {'title':'Timeføring', 'form': form })
from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from models import *
from forms import *
from core.shortcuts import *
from django.contrib import messages
from django.utils.html import escape 

@login_required
def overview(request):
    timetrackings = Timetracking.objects.for_user()    
    return render_with_request(request, 'timetracking/list.html', {'title':'Timeforinger', 'timetrackings':timetrackings})


@login_required
def add(request):
    return form(request)


@login_required
def edit(request, id):
    return form(request, id)


@login_required
def delete(request, id):
    print id
    Timetracking.objects.get(id=id).delete()
    return redirect(overview)


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
def calendar(request):
    return render_with_request(request, "timetracking/calendar.html", {'title':'Timeregistrering' })    


@login_required
def form (request, id = False):
        
    if id:
        instance = get_object_or_404(Timetracking, id = id, deleted=False)
        msg = "Velykket endret timeforing"
    else:
        instance = Timetracking()
        msg = "Velykket lagt til nytt timeforing"
            
    #Save and set to active, require valid form
    if request.method == 'POST':
    
    
        form = TimetrackingForm(request.POST, instance=instance)       
        
        if form.is_valid():    
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            messages.success(request, msg)        

            #Redirects after save for direct editing
            return overview(request)  
        
        
    else:
        form = TimetrackingForm(instance=instance)
    
    return render_with_request(request, "form.html", {'title':'Timeforing', 'form': form })
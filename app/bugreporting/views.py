from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required

from models import *
from forms import *
from core.shortcuts import *
from django.contrib import messages

from django.core.mail import send_mail


@login_required
def overview(request):
    Bugreportings = Bug.objects.all().order_by("closed", "date_created")    
    return render_with_request(request, 'bugreporting/list.html', {'title':'Registrerte bugs', 'bugs':Bugreportings})

@login_required
def add(request):
    return form(request)

@login_required
def view(request, id):
    ticket = Bug.objects.get(id=id)
    comments = BugComment.objects.filter(bug=ticket)
    commentForm = CommentForm(instance = BugComment())
    return render_with_request(request, 'bugreporting/view.html', {'title':ticket.title, 
                                                                   'ticket':ticket,
                                                                   'comments':comments,
                                                                   'commentForm':commentForm})


@login_required
def getRecipientForEmailNoteComment(request, bugID):
    ticket = Bug.objects.get(id=bugID)
    recipients = set([])
    for c in ticket.comments.all():
        recipients.add(c.creator.email)

    recipients.discard(request.user.email)

    return recipients

@login_required
def addComment(request, bugID):

    instance = BugComment()
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=instance)       
        if form.is_valid(): 
            ticket = Bug.objects.get(id=bugID)
            o = form.save(commit=False)
            o.bug = ticket
            o.owner = request.user
            o.save()
            
            send_mail('Ny kommentar til registrert bug %s' % ticket.title, '%s har lagt inn en ny kommentar: \n\n %s' % (request.user, o.text), 
                      'noreply@focussecurity.no', getRecipientForEmailNoteComment(request,bugID), fail_silently=False)

    return redirect(view, bugID)    

@login_required
def changeStatus(request, id):
    ticket = Bug.objects.get(id=id)
    ticket.closed = not ticket.closed
    ticket.save()
    return redirect(view, id)
    
@login_required
def edit(request, id):
    return form(request, id)

@login_required
def delete(request, id):
    return form(request, id)

@login_required
def form (request, id = False):        
    
    if id:
        instance = get_object_or_404(Bug, id = id, deleted=False)
        msg = "Velykket endret bug"
    else:
        instance = Bug()
        msg = "Velykket lagt til ny bug"
        
    #Save and set to active, require valid form
    if request.method == 'POST':

        form = BugreportingForm(request.POST, request.FILES, instance=instance)       
        if form.is_valid():    
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            messages.success(request, msg)
            #Redirects after save for direct editing
            return overview(request)      
    else:
        form = BugreportingForm(instance=instance)
        
    return render_with_request(request, "form.html", {'title':'Bugs', 
                                                      'form': form })
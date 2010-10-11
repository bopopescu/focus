from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required

from models import *
from forms import *
from core.shortcuts import *
from django.contrib import messages
from core.views import updateTimeout
from django.core.mail import send_mail
from django.core import urlresolvers
from settings import SITE_URL

@login_required
def overview(request):
    updateTimeout(request)
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
    
    #Remove the user from notSeenList
    updateNotSeenList(request, id)
    
    return render_with_request(request, 'bugreporting/view.html', {'title':ticket.title, 
                                                                   'ticket':ticket,
                                                                   'comments':comments,
                                                                   'commentForm':commentForm})


def updateNotSeenList(request, bugID):
    ticket = Bug.objects.get(id=bugID)
    notSeen = ticket.usersNotSeenChanges
    notSeen.remove(request.user)
    return

"""
Sends email to all who have written comments in this bugs
Also all of them except the writer to a list, who shows who has not read the changes
or new comment yet.
"""
@login_required
def sendEmailAndUpdateNotSeenList(request, bugID):
    ticket = Bug.objects.get(id=bugID)
    recipients = set([])
    recipientsEmails = set([])
    
    notSeen = ticket.usersNotSeenChanges
    
    #Add the ticket creator to recipients list
    if ticket.creator not in recipients:
        recipients.add(ticket.creator)
    
    #Add the comment creators to recipients list
    for comment in ticket.comments.all():        
        if comment.creator not in ticket.usersNotSeenChanges.all():
            recipients.add(comment.creator)

    #Remove current user, so the current wont get emails and set status to unseen
    recipients.discard(request.user)

    #Set the bug to unseen for all the creators, and add them to email-list    
    #only send email, if they have to seen latest changes
    for user in recipients:              
        if user not in ticket.usersNotSeenChanges.all():
            ticket.usersNotSeenChanges.add(user)
            recipientsEmails.add(user.email)
             
    ticket.save()
    
    

    try:
        link = SITE_URL + urlresolvers.reverse('app.bugreporting.views.view', args=("%s"%ticket.id,))
        send_mail('Ny kommentar, bug %s' % ticket.title, 
                  '%s har lagt inn en ny kommentar i buggen: %s \n\n Direktelink: %s' % (request.user.first_name, ticket.title, link),
                  'time@focussecurity.no', 
                  recipientsEmails, 
                  fail_silently=False)
        
    except:
        print "EMAIL ERROR; CANT SEND EMAIL"

    return recipients    


@login_required
def addComment(request, bugID):

    instance = BugComment()
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=instance)       
        if form.is_valid(): 
            ticket = Bug.objects.get(id=bugID)
            o = form.save(commit=False)
            o.bug = ticket
            o.owner = request.user
            o.save()
            
            if ticket.closed:
                ticket.closed = not ticket.closed
                
            sendEmailAndUpdateNotSeenList(request, bugID)
            ticket.save()
            
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
        msg = "Vellykket lagt til ny bug"
        
    print "OK"
    
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
from core.shortcuts import *

def overview(request):
    return render(request, 'mail/dailyNotifications.html')
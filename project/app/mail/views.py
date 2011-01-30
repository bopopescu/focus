from core.shortcuts import *

def overview(request):
    return render_with_request(request, 'mail/dailyNotifications.html')
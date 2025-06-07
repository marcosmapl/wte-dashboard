from django.shortcuts import render


def dashboard_services(request):
    return render(request, "dashboard/index.html")
    # unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    # unread_notification_count = unread_notification.count()
    
def dashboard_general(request):
    return render(request, "Home/index.html")

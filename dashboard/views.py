from django.shortcuts import render


def dashboard_booking(request):
    return render(request, "dashboard/dashboard-booking.html")
    # unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    # unread_notification_count = unread_notification.count()
    
def dashboard_general(request):
    return render(request, "dashboard/dashboard-general.html")

from django.shortcuts import render
from django.db.models import Sum, Q, Count

from booking.models import Booking, BookingStatus
from financial.models import CustomerInvoice, PartnerInvoice


def dashboard_general(request):
    confirmed_count = Booking.objects.filter(status=BookingStatus.CONFIRMED).count()
    canceled_count = Booking.objects.filter(
        Q(status=BookingStatus.CANCELLED_BY_PARTNER) | Q(status=BookingStatus.CANCELLED_BY_CLIENT)
    ).count()
    income_sum = CustomerInvoice.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    outcome_sum = PartnerInvoice.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    
    context = {
        'confirmed_count': confirmed_count,
        'canceled_count': canceled_count,
        'income_sum': income_sum,
        'outcome_sum': outcome_sum,
    }
    return render(request, "dashboard/dashboard-general.html", context)


def dashboard_booking(request):
    return render(request, "dashboard/dashboard-booking.html")
    # unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    # unread_notification_count = unread_notification.count()
    

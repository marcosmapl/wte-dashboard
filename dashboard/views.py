from django.shortcuts import render, redirect
from django.db.models import Sum, Q, Count

from booking.models import Booking, BookingStatus
from financial.models import CustomerInvoice, PartnerInvoice
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_general(request):
    user = request.user
    if not user.is_active or not user.is_general_manager:
        return redirect('index')

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


@login_required
def dashboard_booking(request):
    user = request.user
    if not user.is_active or not user.is_general_manager:
        return redirect('index')

    return render(request, "dashboard/dashboard-booking.html")
    # unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    # unread_notification_count = unread_notification.count()
    

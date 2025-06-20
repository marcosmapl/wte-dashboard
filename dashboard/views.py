from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q, Count
from django.db.models.functions import TruncDate
from django.forms import DateField, DateTimeField
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from django.views.decorators.http import require_GET

from booking.models import Booking, BookingStatus
from financial.models import CustomerInvoice, InvoiceStatus, PartnerInvoice

from datetime import timedelta, datetime


@login_required
def dashboard_general(request):
    user = request.user
    if not user.is_active or not user.is_general_manager:
        return redirect('index')

    income_sum = CustomerInvoice.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    outcome_sum = PartnerInvoice.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    
    interval = request.GET.get('interval', '7')  # padrão: 7 dias
    try:
        days = int(interval)
    except ValueError:
        days = 7
        
    today = timezone.now()
    limit_date = today + timedelta(days=days)
    
    # Filtrar reservas futuras confirmadas dentro do intervalo
    upcoming_bookings = Booking.objects.filter(
        # status=BookingStatus.CONFIRMED,
        experience_date__range=(today, limit_date)
    ).order_by('experience_date')
    
    try:
        start_date = datetime.strptime(request.GET.get('start'), '%Y-%m-%d')
        end_date = datetime.strptime(request.GET.get('end'), '%Y-%m-%d')
    except (TypeError, ValueError):
        # Fallback: últimos 30 dias
        start_date = today
        end_date = today + timezone.timedelta(days=7)

    # Agrupar por status
    list_bookings_by_status = (
        Booking.objects
        .filter(experience_date__range=(start_date, end_date))
        .values('status')
        .annotate(total=Count('id'))
        .order_by('status')
    )
    
    dict_bookings_by_status = {item['status']:item['total'] for item in list_bookings_by_status}
    
    context = {
        'confirmed_count': dict_bookings_by_status.get(BookingStatus.CONFIRMED.label, 0),
        'canceled_count': dict_bookings_by_status.get(BookingStatus.CANCELLED_BY_CLIENT.label,0 ) + dict_bookings_by_status.get(BookingStatus.CANCELLED_BY_PARTNER.label, 0),
        'pending_count': dict_bookings_by_status.get(BookingStatus.PENDING.label, 0),
        'income_sum': income_sum,
        'outcome_sum': outcome_sum,
        'interval': days,
        'upcoming_bookings': upcoming_bookings,
        'start_date': start_date.date(),
        'end_date': end_date.date(),
    }
    return render(request, "dashboard/dashboard-general.html", context)


@login_required
def ajax_upcoming_bookings(request):
    # if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     return JsonResponse({'error': 'Requisição inválida'}, status=400)
    
    days = int(request.GET.get('interval', 7))
    today = timezone.now()
    limit_date = today + timedelta(days=days)

    bookings = Booking.objects.filter(
        # status=BookingStatus.CONFIRMED,
        experience_date__range=(today, limit_date)
    ).order_by('experience_date')

    html = render_to_string("dashboard/partials/upcoming-bookings-tbody.html", {
        'upcoming_bookings': bookings
    })

    return JsonResponse({'html': html})


@login_required
def ajax_general_monitor_count(request):
    days = int(request.GET.get('interval', 7))
    
    today = timezone.now()
    limit_date = today + timedelta(days=days)

    income_sum = CustomerInvoice.objects.filter(
        status=InvoiceStatus.PAID,
        paid_date__range=(today, limit_date)
    ).aggregate(total_sum=Sum('total_amount'))['total_sum'] or 0

    outcome_sum = PartnerInvoice.objects.filter(
        status=InvoiceStatus.PAID,
        paid_date__range=(today, limit_date)
    ).aggregate(total_sum=Sum('total_amount'))['total_sum'] or 0
 
    # Agrupar por status
    list_bookings_by_status = (
        Booking.objects
        .filter(experience_date__range=(today, limit_date))
        .values('status')
        .annotate(total=Count('id'))
        .order_by('status')
    )

    dict_bookings_by_status = {item['status']:item['total'] for item in list_bookings_by_status}

    html = render_to_string("dashboard/partials/general-count-monitor.html", {
        'confirmed_count': dict_bookings_by_status.get(BookingStatus.CONFIRMED.label, 0),
        'canceled_count': dict_bookings_by_status.get(BookingStatus.CANCELLED_BY_CLIENT.label,0 ) + dict_bookings_by_status.get(BookingStatus.CANCELLED_BY_PARTNER.label, 0),
        'pending_count': dict_bookings_by_status.get(BookingStatus.PENDING.label, 0),
        'income_sum': income_sum,
        'outcome_sum': outcome_sum,
    })

    return JsonResponse({'html': html})


require_GET
def ajax_bookings_by_status_and_day(request):
    start_date = parse_date(request.GET.get("start"))
    end_date = parse_date(request.GET.get("end"))

    if not start_date or not end_date or start_date > end_date:
        return JsonResponse({"error": "Parâmetros de data inválidos."}, status=400)

    # Converter para datetime aware com fuso horário
    start_dt = make_aware(datetime.combine(start_date, datetime.min.time()))
    end_dt = make_aware(datetime.combine(end_date, datetime.max.time()))

    # Lista de dias no intervalo
    num_days = (end_date - start_date).days + 1
    day_list = [(start_date + timedelta(days=i)).strftime("%d-%m-%Y") for i in range(num_days)]

    # Inicializa estrutura de resposta
    result = {
        "days": day_list,
        BookingStatus.CONFIRMED.label: [0] * num_days,
        BookingStatus.PENDING.label: [0] * num_days,
        BookingStatus.CANCELLED_BY_CLIENT.label: [0] * num_days,
        BookingStatus.CANCELLED_BY_PARTNER.label: [0] * num_days,
    }

    # Query agregada por dia e status
    bookings = (
        Booking.objects
        .filter(experience_date__range=(start_dt, end_dt), experience_date__isnull=False)
        .annotate(day=TruncDate('experience_date', output_field=DateField()))
        .values('day', 'status')
        .annotate(count=Count('id'))
    )

    for entry in bookings:
        day = entry.get("day")
        if day is None:
            continue

        day_str = day.strftime("%d-%m-%Y")
        status = entry["status"]
        count = entry["count"]

        if day_str in result["days"] and status in result:
            index = result["days"].index(day_str)
            result[status][index] += count

    return JsonResponse(result)


@login_required
def dashboard_booking(request):
    user = request.user
    if not user.is_active or not user.is_general_manager:
        return redirect('index')

    return render(request, "dashboard/dashboard-booking.html")
    # unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    # unread_notification_count = unread_notification.count()
    

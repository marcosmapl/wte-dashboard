from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import get_object_or_404

from booking.models import Booking, BookingChannel, BookingStatus
from experience.models import Experience, Partner


@login_required
def list_booking_view(request):
    user = request.user
    if not user.is_active or not user.is_booking_agent:
        return redirect('index')

    booking_list = Booking.objects.select_related('experience', 'partner').all()
    # print(f"Booking list: {booking_list}")
    context = {
        'page_mode': 'list',
        'booking_list': booking_list,
    }
    return render(request, "booking/list-booking.html", context)


@login_required
def add_booking_view(request):
    user = request.user
    if not user.is_active or not user.is_booking_agent:
        return redirect('index')

    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")
        
        # Criação do objeto
        booking = Booking(
            code=request.POST.get('booking_code'),
            client_name=request.POST.get('booking_client_name'),
            client_nif=request.POST.get('booking_client_nif'),
            client_email=request.POST.get('booking_client_email'),
            client_phone=request.POST.get('booking_client_phone'),
            experience_date=request.POST.get('booking_experience_date'),
            number_adults=request.POST.get('booking_number_adults', 1),
            number_children=request.POST.get('booking_number_children', 0),
            price_adults=request.POST.get('booking_price_adults', 1),
            price_children=request.POST.get('booking_price_children', 0),
            discount=request.POST.get('booking_discount', 0),
            total=request.POST.get('booking_total', 1),
            channel=request.POST.get('booking_channel', BookingChannel.WORDPRESS),
            status=request.POST.get('booking_status', BookingStatus.PENDING),
            experience=Experience.objects.get(id=request.POST.get('booking_experience')),
            partner=Partner.objects.get(id=request.POST.get('booking_partner')),
            created_by=request.user,
            updated_by=request.user
        )
        
        try:
            # Validação do objeto
            booking.full_clean()
            
            # Salva o objeto no banco de dados
            booking.save()
            
            #TODO: show message popup
            messages.success(request, "Reserva realizada com sucesso.")
            return redirect('list_booking')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                messages.error(request, f"Erro de validação: {".".join(errors)}")
                break            
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")

    e_list = Experience.objects.all().order_by('title')
    p_list = Partner.objects.all().order_by('name')

    context = {
        'experience_list': e_list,
        'experience_selected': e_list[0] if e_list else None,
        'partner_list': p_list,
        'partner_selected': p_list[0] if p_list else None,
        'channel_options': BookingChannel.choices,
        'channel_selected': BookingChannel.WORDPRESS,
        'status_options': BookingStatus.choices,
        'status_selected': BookingStatus.PENDING,
    }
    
    # TODO: add error message popup
    return render(request, "booking/add-booking.html", context)


@login_required
def edit_booking_view(request, id):
    user = request.user
    if not user.is_active or not user.is_booking_agent:
        return redirect('index')

    booking = Booking.objects.select_related('experience', 'partner').get(id=id)
    
    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")

        # Atualiza os campos do objeto
        booking.code = request.POST.get('booking_code')
        booking.client_name = request.POST.get('booking_client_name')
        booking.client_nif = request.POST.get('booking_client_nif')
        booking.client_email = request.POST.get('booking_client_email')
        booking.client_phone = request.POST.get('booking_client_phone')
        booking.experience_date = request.POST.get('booking_experience_date')
        booking.number_adults = request.POST.get('booking_number_adults', 1)
        booking.number_children = request.POST.get('booking_number_children', 0)
        booking.price_adults = request.POST.get('booking_price_adults', 1)
        booking.price_children = request.POST.get('booking_price_children', 0)
        booking.discount = request.POST.get('booking_discount', 0)
        booking.total = request.POST.get('booking_total', 1)
        booking.channel = request.POST.get('booking_channel', BookingChannel.WORDPRESS)
        booking.status = request.POST.get('booking_status', BookingStatus.PENDING)
        booking.experience = Experience.objects.get(id=request.POST.get('booking_experience'))
        booking.partner = Partner.objects.get(id=request.POST.get('booking_partner'))
        booking.updated_by = request.user
        booking.updated_at = None # Reseta o campo modified_at para que seja atualizado no save()
        
        try:
            # Validação do objeto
            booking.full_clean()
            
            # Salva o objeto no banco de dados
            booking.save()
            
            messages.success(request, "Reserva atualizada com sucesso.")
            return redirect('list_booking')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                messages.error(request, f"Erro de validação: {".".join(errors)}")
                break            
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
    
    # print(f"Experience details: {experience.category}, {experience.status}")
    e_list = Experience.objects.all().order_by('title')
    p_list = Partner.objects.all().order_by('name')
    context = {
        'page_mode': 'edit',
        'booking': booking,
        'experience_list': e_list,
        'experience_selected': booking.experience,
        'partner_list': p_list,
        'partner_selected': booking.partner,
        'channel_options': BookingChannel.choices,
        'channel_selected': str(booking.channel),
        'status_options': BookingStatus.choices,
        'status_selected': str(booking.status),
    }
    
    return render(request, "booking/edit-booking.html", context)


@login_required
def delete_booking_view(request, id):
    user = request.user
    if not user.is_active or not user.is_booking_agent:
        return redirect('index')
    
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=id)
        # Verifica se o objeto existe
        if not booking:
            messages.error(request, "Reserva não encontrada.")
        else:
            # Exclui o objeto
            booking.delete()
            messages.success(request, "Reserva excluída com sucesso.")    
    
    return redirect('list_booking')


@login_required
def view_booking(request, id):
    user = request.user
    if not user.is_active or not user.is_booking_agent:
        return redirect('index')
    
    booking = Booking.objects.select_related('experience', 'partner').get(id=id)

    print(type(booking.customer_invoice))
    print(booking)
    return render(request, 'booking/view-booking.html', {'booking': booking})

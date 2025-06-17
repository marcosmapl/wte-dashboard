from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from booking.models import Booking
from financial.models import CustomerInvoice, InvoiceStatus, PartnerInvoice, PaymentMethod
from home_auth.models import WineUser


def list_customer_invoice_view(request):
    invoice_list = CustomerInvoice.objects.select_related('booking').all()
    # print(f"Booking list: {booking_list}")
    context = {
        'page_mode': 'list',
        'invoice_list': invoice_list,
    }
    return render(request, "financial/list-customer-invoice.html", context)


def add_customer_invoice_view(request):
    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")
        print(request.POST)
        # Criação do objeto
        invoice = CustomerInvoice(
            code=request.POST.get('customer_invoice_code'),
            emission_date=request.POST.get('customer_invoice_emission_date'),
            payment_date=request.POST.get('customer_invoice_payment_date'),
            paid_date=request.POST.get('customer_invoice_paid_date'),
            total_amount=request.POST.get('customer_invoice_total_amount'),
            file_link=request.POST.get('customer_invoice_file_link'),
            payment_method=request.POST.get('customer_invoice_payment_method', PaymentMethod.BANK_TRANSFER),
            status=request.POST.get('customer_invoice_status', InvoiceStatus.PENDING),
            booking=Booking.objects.get(id=request.POST.get('customer_invoice_booking')),
            created_by=request.user,
            updated_by=request.user,
        )
        
        try:
            # Validação do objeto
            invoice.full_clean()
            
            # Salva o objeto no banco de dados
            invoice.save()
            
            #TODO: show message popup
            messages.success(request, "Fatura cadastrada com sucesso.")
            return redirect('list_customer_invoice')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                messages.error(request, f"Erro de validação: {".".join(errors)}")
                print(field)
                print(errors)
                break            
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
            print(e)

    b_list = Booking.objects.all().order_by('code')

    context = {
        'booking_list': b_list,
        'booking_selected': b_list[0] if b_list else None,
        'payment_method_options': PaymentMethod.choices,
        'payment_method_selected': PaymentMethod.BANK_TRANSFER,
        'status_options': InvoiceStatus.choices,
        'status_selected': InvoiceStatus.PENDING,
    }
    
    # TODO: add error message popup
    return render(request, "financial/add-customer-invoice.html", context)
              

def edit_customer_invoice_view(request, id):
    invoice = CustomerInvoice.objects.select_related('booking').get(id=id)
    
    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")

        # Atualiza os campos do objeto
        invoice.code = request.POST.get('customer_invoice_code')
        invoice.emission_date = request.POST.get('customer_invoice_emission_date')
        invoice.payment_date = request.POST.get('customer_invoice_payment_date')
        invoice.paid_date = request.POST.get('customer_invoice_paid_date')
        invoice.total_amount = request.POST.get('customer_invoice_total_amount')
        invoice.file_link = request.POST.get('customer_invoice_file_link')
        invoice.payment_method = request.POST.get('customer_invoice_payment_method')
        invoice.status = request.POST.get('customer_invoice_status')
        invoice.booking = Booking.objects.get(id=request.POST.get('customer_invoice_booking'))
        invoice.created_by = request.user
        invoice.updated_by = request.user
        invoice.updated_at = None # Reseta o campo modified_at para que seja atualizado no save()
        
        try:
            # Validação do objeto
            invoice.full_clean()
            
            # Salva o objeto no banco de dados
            invoice.save()
            
            messages.success(request, "Reserva atualizada com sucesso.")
            return redirect('list_customer_invoice')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                messages.error(request, f"Erro de validação: {".".join(errors)}")
                break            
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
    
    # print(f"Experience details: {experience.category}, {experience.status}")
    b_list = Booking.objects.all().order_by('code')
    context = {
        'page_mode': 'edit',
        'customer_invoice': invoice,
        'booking_list': b_list,
        'booking_selected': b_list[0] if b_list else None,
        'payment_method_options': PaymentMethod.choices,
        'payment_method_selected': str(invoice.payment_method),
        'status_options': InvoiceStatus.choices,
        'status_selected': str(invoice.status),
    }
    
    return render(request, "financial/edit-customer-invoice.html", context)


def delete_customer_invoice_view(request, id):
    if request.method == "POST":
        invoice = get_object_or_404(CustomerInvoice, id=id)
        # Verifica se o objeto existe
        if not invoice:
            messages.error(request, "Fatura não encontrada.")
        else:
            # Exclui o objeto
            invoice.delete()
            messages.success(request, "Fatura excluída com sucesso.")    
    
    return redirect('list_customer_invoice')


def list_partner_invoice_view(request):
    invoice_list = PartnerInvoice.objects.select_related('booking').all()
    # print(f"Booking list: {booking_list}")
    context = {
        'page_mode': 'list',
        'invoice_list': invoice_list,
    }
    return render(request, "financial/list-partner-invoice.html", context)


def add_partner_invoice_view(request):
    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")
        print(request.POST)
        # Criação do objeto
        invoice = PartnerInvoice(
            code=request.POST.get('partner_invoice_code'),
            emission_date=request.POST.get('partner_invoice_emission_date'),
            payment_date=request.POST.get('partner_invoice_payment_date'),
            paid_date=request.POST.get('partner_invoice_paid_date'),
            total_amount=request.POST.get('partner_invoice_total_amount'),
            file_link=request.POST.get('partner_invoice_file_link'),
            payment_method=request.POST.get('partner_invoice_payment_method', PaymentMethod.BANK_TRANSFER),
            status=request.POST.get('partner_invoice_status', InvoiceStatus.PENDING),
            booking=Booking.objects.get(id=request.POST.get('partner_invoice_booking')),
            created_by=request.user,
            updated_by=request.user,
        )
        
        try:
            # Validação do objeto
            invoice.full_clean()
            
            # Salva o objeto no banco de dados
            invoice.save()
            
            #TODO: show message popup
            messages.success(request, "Fatura cadastrada com sucesso.")
            return redirect('list_partner_invoice')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                messages.error(request, f"Erro de validação: {".".join(errors)}")
                print(field)
                print(errors)
                break            
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
            print(e)

    b_list = Booking.objects.all().order_by('code')

    context = {
        'booking_list': b_list,
        'booking_selected': b_list[0] if b_list else None,
        'payment_method_options': PaymentMethod.choices,
        'payment_method_selected': PaymentMethod.BANK_TRANSFER,
        'status_options': InvoiceStatus.choices,
        'status_selected': InvoiceStatus.PENDING,
    }
    
    # TODO: add error message popup
    return render(request, "financial/add-partner-invoice.html", context)
              

def edit_partner_invoice_view(request, id):
    invoice = PartnerInvoice.objects.select_related('booking').get(id=id)
    
    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")

        # Atualiza os campos do objeto
        invoice.code = request.POST.get('partner_invoice_code')
        invoice.emission_date = request.POST.get('partner_invoice_emission_date')
        invoice.payment_date = request.POST.get('partner_invoice_payment_date')
        invoice.paid_date = request.POST.get('partner_invoice_paid_date')
        invoice.total_amount = request.POST.get('partner_invoice_total_amount')
        invoice.file_link = request.POST.get('partner_invoice_file_link')
        invoice.payment_method = request.POST.get('partner_invoice_payment_method')
        invoice.status = request.POST.get('partner_invoice_status')
        invoice.booking = Booking.objects.get(id=request.POST.get('partner_invoice_booking'))
        invoice.created_by = request.user
        invoice.updated_by = request.user
        invoice.updated_at = None # Reseta o campo modified_at para que seja atualizado no save()
        
        try:
            # Validação do objeto
            invoice.full_clean()
            
            # Salva o objeto no banco de dados
            invoice.save()
            
            messages.success(request, "Reserva atualizada com sucesso.")
            return redirect('list_partner_invoice')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                messages.error(request, f"Erro de validação: {".".join(errors)}")
                break            
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
    
    # print(f"Experience details: {experience.category}, {experience.status}")
    b_list = Booking.objects.all().order_by('code')
    context = {
        'page_mode': 'edit',
        'partner_invoice': invoice,
        'booking_list': b_list,
        'booking_selected': b_list[0] if b_list else None,
        'payment_method_options': PaymentMethod.choices,
        'payment_method_selected': str(invoice.payment_method),
        'status_options': InvoiceStatus.choices,
        'status_selected': str(invoice.status),
    }
    
    return render(request, "financial/edit-partner-invoice.html", context)


def delete_partner_invoice_view(request, id):
    if request.method == "POST":
        invoice = get_object_or_404(PartnerInvoice, id=id)
        # Verifica se o objeto existe
        if not invoice:
            messages.error(request, "Fatura não encontrada.")
        else:
            # Exclui o objeto
            invoice.delete()
            messages.success(request, "Fatura excluída com sucesso.")    
    
    return redirect('list_partner_invoice')

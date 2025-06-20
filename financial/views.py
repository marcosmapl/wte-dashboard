from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from booking.models import Booking
from financial.models import CustomerInvoice, InvoiceStatus, PartnerInvoice, PaymentMethod


@login_required
def list_customer_invoice_view(request):
    user = request.user
    if not user.is_active or not user.is_general_manager:
        return redirect('index')

    invoice_list = CustomerInvoice.objects.all()

    context = {
        'invoice_list': invoice_list,
    }
    return render(request, "financial/list-customer-invoice.html", context)


@login_required
def add_customer_invoice_view(request, booking_id):
    user = request.user
    if not user.is_active or not user.is_general_manager:
        return redirect('index')
    
    booking=Booking.objects.get(id=booking_id)

    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")
        print(request.POST)
        # Criação do objeto
        invoice = CustomerInvoice(
            code=request.POST.get('invoice_code'),
            emission_date=request.POST.get('invoice_emission_date'),
            payment_date=request.POST.get('invoice_payment_date'),
            paid_date=request.POST.get('invoice_paid_date'),
            service_value=request.POST.get('invoice_service_value'),
            taxes_value=request.POST.get('invoice_taxes_value'),
            discount_value=request.POST.get('invoice_discount_value'),
            total_amount=request.POST.get('invoice_total_amount'),
            file_link=request.POST.get('invoice_file_link'),
            payment_method=request.POST.get('invoice_payment_method', PaymentMethod.BANK_TRANSFER),
            status=request.POST.get('invoice_status', InvoiceStatus.PENDING),
            booking=Booking.objects.get(id=booking_id),
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

    context = {
        'booking': booking,
        'payment_method_options': PaymentMethod.choices,
        'payment_method_selected': PaymentMethod.BANK_TRANSFER,
        'status_options': InvoiceStatus.choices,
        'status_selected': InvoiceStatus.PENDING,
    }
    
    # TODO: add error message popup
    return render(request, "financial/add-customer-invoice.html", context)
              

@login_required
def edit_customer_invoice_view(request, id):
    user = request.user
    if not user.is_active or not user.is_general_manager:
        return redirect('index')

    invoice = CustomerInvoice.objects.select_related('booking').get(id=id)
    
    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")

        # Atualiza os campos do objeto
        invoice.code = request.POST.get('invoice_code')
        invoice.emission_date = request.POST.get('invoice_emission_date')
        invoice.payment_date = request.POST.get('invoice_payment_date')
        invoice.paid_date = request.POST.get('invoice_paid_date')
        invoice.service_value = request.POST.get('invoice_service_value')
        invoice.taxes_value = request.POST.get('invoice_taxes_value')
        invoice.discount_value = request.POST.get('invoice_discount_value')
        invoice.total_amount = request.POST.get('invoice_total_amount')
        invoice.file_link = request.POST.get('invoice_file_link')
        invoice.payment_method = request.POST.get('invoice_payment_method')
        invoice.status = request.POST.get('invoice_status')
        invoice.created_by = request.user
        invoice.updated_by = request.user
        invoice.updated_at = None # Reseta o campo modified_at para que seja atualizado no save()
        
        try:
            # Validação do objeto
            invoice.full_clean()
            
            # Salva o objeto no banco de dados
            invoice.save()
            
            messages.success(request, "Fatura atualizada com sucesso.")
            return redirect('list_customer_invoice')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                messages.error(request, f"Erro de validação: {".".join(errors)}")
                break            
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
    
    context = {
        'invoice': invoice,
        'payment_method_options': PaymentMethod.choices,
        'payment_method_selected': str(invoice.payment_method),
        'status_options': InvoiceStatus.choices,
        'status_selected': str(invoice.status),
    }
    
    return render(request, "financial/edit-customer-invoice.html", context)


@login_required
def delete_customer_invoice_view(request, id):
    user = request.user
    if not user.is_active or not user.is_general_manager:
        return redirect('index')

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


@login_required
def customer_invoice_view(request, id):
    user = request.user
    if not user.is_active or not user.is_booking_agent:
        return redirect('index')
    
    invoice = CustomerInvoice.objects.get(id=id)
    print(invoice)
    return render(request, 'financial/view-customer-invoice.html', {
        'invoice': invoice,
        'booking': invoice.booking
    })


@login_required
def list_partner_invoice_view(request):
    user = request.user
    if not user.is_active or not user.is_general_manager:
        return redirect('index')
    
    invoice_list = PartnerInvoice.objects.all()

    context = {
        'invoice_list': invoice_list,
    }
    return render(request, "financial/list-partner-invoice.html", context)


@login_required
def add_partner_invoice_view(request, booking_id):
    user = request.user
    if not user.is_active or not user.is_general_manager:
        return redirect('index')
    
    booking=Booking.objects.get(id=booking_id)

    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")
        print(request.POST)
        # Criação do objeto
        invoice = PartnerInvoice(
            code=request.POST.get('invoice_code'),
            emission_date=request.POST.get('invoice_emission_date'),
            payment_date=request.POST.get('invoice_payment_date'),
            paid_date=request.POST.get('invoice_paid_date'),
            service_value=request.POST.get('invoice_service_value'),
            taxes_value=request.POST.get('invoice_taxes_value'),
            discount_value=request.POST.get('invoice_discount_value'),
            total_amount=request.POST.get('invoice_total_amount'),
            file_link=request.POST.get('invoice_file_link'),
            payment_method=request.POST.get('invoice_payment_method', PaymentMethod.BANK_TRANSFER),
            status=request.POST.get('invoice_status', InvoiceStatus.PENDING),
            booking=Booking.objects.get(id=booking_id),
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
                break            
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")

    context = {
        'booking': booking,
        'payment_method_options': PaymentMethod.choices,
        'payment_method_selected': PaymentMethod.BANK_TRANSFER,
        'status_options': InvoiceStatus.choices,
        'status_selected': InvoiceStatus.PENDING,
    }
    
    # TODO: add error message popup
    return render(request, "financial/add-partner-invoice.html", context)
              

@login_required
def edit_partner_invoice_view(request, id):
    user = request.user
    if not user.is_active or not user.is_general_manager:
        return redirect('index')

    invoice = PartnerInvoice.objects.select_related('booking').get(id=id)
    
    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")

        # Atualiza os campos do objeto
        invoice.code = request.POST.get('invoice_code')
        invoice.emission_date = request.POST.get('invoice_emission_date')
        invoice.payment_date = request.POST.get('invoice_payment_date')
        invoice.paid_date = request.POST.get('invoice_paid_date')
        invoice.service_value = request.POST.get('invoice_service_value')
        invoice.taxes_value = request.POST.get('invoice_taxes_value')
        invoice.discount_value = request.POST.get('invoice_discount_value')
        invoice.total_amount = request.POST.get('invoice_total_amount')
        invoice.file_link = request.POST.get('invoice_file_link')
        invoice.payment_method = request.POST.get('invoice_payment_method')
        invoice.status = request.POST.get('invoice_status')
        invoice.created_by = request.user
        invoice.updated_by = request.user
        invoice.updated_at = None # Reseta o campo modified_at para que seja atualizado no save()
        
        try:
            # Validação do objeto
            invoice.full_clean()
            
            # Salva o objeto no banco de dados
            invoice.save()
            
            messages.success(request, "Fatura atualizada com sucesso.")
            return redirect('list_partner_invoice')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                messages.error(request, f"Erro de validação: {".".join(errors)}")
                break            
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
    
    context = {
        'invoice': invoice,
        'payment_method_options': PaymentMethod.choices,
        'payment_method_selected': str(invoice.payment_method),
        'status_options': InvoiceStatus.choices,
        'status_selected': str(invoice.status),
    }
    
    return render(request, "financial/edit-partner-invoice.html", context)


@login_required
def delete_partner_invoice_view(request, id):
    user = request.user
    if not user.is_active or not user.is_general_manager:
        return redirect('index')
    
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

@login_required
def partner_invoice_view(request, id):
    user = request.user
    if not user.is_active or not user.is_booking_agent:
        return redirect('index')
    
    invoice = PartnerInvoice.objects.get(id=id)
    return render(request, 'financial/view-partner-invoice.html', {
        'invoice': invoice,
        'booking': invoice.booking,
    })

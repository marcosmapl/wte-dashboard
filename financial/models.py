from django.db import models

from booking.models import Booking
from home_auth.models import WineUser

class PaymentMethod(models.TextChoices):
    BANK_TRANSFER = 'Referência Multibanco', 'Referência Multibanco'
    CREDIT_CARD = 'Cartão de Crédito', 'Cartão de Crédito'
    DEBIT_CARD = 'Cartão de Débito', 'Cartão de Débito'
    MBWAY = 'MB WAY', 'MB WAY'
    CASH = 'Dinheiro', 'Dinheiro'


class InvoiceStatus(models.TextChoices):
    PENDING = 'Pendente', 'Pendente'
    PAID = 'Paga', 'Paga'
    CANCELLED = 'Cancelada', 'Cancelada'
    OVERDUE = 'Vencida', 'Vencida'


class CustomerInvoice(models.Model):
    code = models.CharField(max_length=13, db_index=True, unique=True)
    emission_date = models.DateField()
    payment_date = models.DateField()
    paid_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    file_link = models.TextField()
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices, default=PaymentMethod.BANK_TRANSFER)
    status = models.CharField(max_length=30, choices=InvoiceStatus.choices, default=InvoiceStatus.PENDING)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(WineUser, on_delete=models.SET_NULL, null=True, db_index=True, related_name='civc_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(WineUser, on_delete=models.SET_NULL, null=True, db_index=True, related_name='civc_updated_by')
    
    def __str__(self):
        return f"{self.code} - {self.booking.client_name}"


class PartnerInvoice(models.Model):
    code = models.CharField(max_length=13, db_index=True, unique=True)
    emission_date = models.DateField()
    payment_date = models.DateField()
    paid_date = models.DateField()
    file_link = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices, default=PaymentMethod.BANK_TRANSFER)
    status = models.CharField(max_length=30, choices=InvoiceStatus.choices, default=InvoiceStatus.PENDING)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, db_index=True, related_name='partner_invoices')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(WineUser, on_delete=models.SET_NULL, null=True, db_index=True, related_name='pivc_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(WineUser, on_delete=models.SET_NULL, null=True, db_index=True, related_name='pivc_updated_by')

    def __str__(self):
        return f"{self.code} - {self.booking.partner.name}"

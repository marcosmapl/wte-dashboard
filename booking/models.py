from django.db import models

from experience.models import Experience, Partner
from home_auth.models import WineUser

# Create your models here.

class BookingChannel(models.TextChoices):
    FACEBOOK = 'Facebook', 'Facebook'
    INSTAGRAM = 'Instagram', 'Instagram'
    WORDPRESS = 'Wordpress', 'Wordpress'
    WHATSAPP = 'Whatsapp', 'Whatsapp'


class BookingStatus(models.TextChoices):
    PENDING = 'Pendente', 'Pendente'
    CONFIRMED = 'Confirmada', 'Confirmada'
    CANCELLED_BY_CLIENT = 'Cancelada (Cliente)', 'Cancelada (Cliente)'
    CANCELLED_BY_PARTNER = 'Cancelada (Parceiro)', 'Cancelada (Parceiro)'


class Booking(models.Model):
    code = models.CharField(max_length=13, db_index=True, unique=True)
    client_name = models.CharField(max_length=100, db_index=True)
    client_nif = models.CharField(max_length=30, db_index=True, null=True, blank=True)
    client_email = models.EmailField(max_length=255, db_index=True, null=True, blank=True)
    client_phone = models.CharField(max_length=15, null=True, blank=True)
    experience_date = models.DateTimeField()
    number_adults = models.PositiveIntegerField(default=1)
    number_children = models.PositiveIntegerField(default=0)
    price_adults = models.DecimalField(max_digits=10, decimal_places=2)
    price_children = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    channel = models.CharField(max_length=20, choices=BookingChannel.choices, default=BookingChannel.WORDPRESS)
    status = models.CharField(max_length=30, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='booking_experience')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='booking_partner')
    reserved_by = models.ForeignKey(WineUser, on_delete=models.CASCADE, related_name='booking_user')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reserva de {self.client_name} ({self.code})"


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
    reservation = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='customer_invoice_booking')
    created_by = models.ForeignKey(WineUser, on_delete=models.CASCADE, related_name='customer_invoice_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fatura Cliente {self.reservation.client_name} ({self.code})"


class PartnerInvoice(models.Model):
    code = models.CharField(max_length=13, db_index=True, unique=True)
    emission_date = models.DateField()
    payment_date = models.DateField()
    paid_date = models.DateField()
    file_link = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices, default=PaymentMethod.BANK_TRANSFER)
    status = models.CharField(max_length=30, choices=InvoiceStatus.choices, default=InvoiceStatus.PENDING)
    reservation = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='partner_invoice_booking')
    created_by = models.ForeignKey(WineUser, on_delete=models.CASCADE, related_name='partner_invoice_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fatura Parceiro: {self.reservation.partner.name} ({self.code})"

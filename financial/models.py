from django.db import models

from WineTour import settings
from booking.models import Booking
from home_auth.models import WineUser

class PaymentMethod(models.TextChoices):
    CREDIT_CARD = 'Cartão de Crédito', 'Cartão de Crédito'
    DEBIT_CARD = 'Cartão de Débito', 'Cartão de Débito'
    CASH = 'Dinheiro', 'Dinheiro'
    IBAN = 'IBAN', 'IBAN'
    MBWAY = 'MB WAY', 'MB WAY'
    BANK_TRANSFER = 'Referência Multibanco', 'Referência Multibanco'


class InvoiceStatus(models.TextChoices):
    PENDING = 'Pendente', 'Pendente'
    PAID = 'Pago', 'Pago'
    CANCELLED = 'Cancelado', 'Cancelado'
    OVERDUE = 'Vencido', 'Vencido'


class BaseInvoice(models.Model):
    code = models.CharField(max_length=13, db_index=True, unique=True)
    emission_date = models.DateTimeField()
    payment_date = models.DateTimeField()
    paid_date = models.DateTimeField()
    file_link = models.TextField()
    service_value = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=1.0)
    taxes_value = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.0)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=1.0)
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices, default=PaymentMethod.BANK_TRANSFER)
    status = models.CharField(max_length=30, choices=InvoiceStatus.choices, default=InvoiceStatus.PENDING)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(WineUser, on_delete=models.SET_NULL, null=True, db_index=True, related_name="%(class)s_created_by")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(WineUser, on_delete=models.SET_NULL, null=True, db_index=True, related_name="%(class)s_updated_by")

    class Meta:
        abstract = True

    @property
    def emission_date_str(self):
        return self.emission_date.strftime(settings.DATETIME_FORMAT_STR)

    @property
    def payment_date_str(self):
        return self.payment_date.strftime(settings.DATETIME_FORMAT_STR)

    @property
    def paid_date_str(self):
        return self.paid_date.strftime(settings.DATETIME_FORMAT_STR)

    @property
    def service_value_str(self):
        return str(self.service_value).replace(",", ".")

    @property
    def service_value_money(self):
        return "Є " + str(self.service_value).replace(",", ".")

    @property
    def taxes_value_str(self):
        return str(self.taxes_value).replace(",", ".")

    @property
    def taxes_value_money(self):
        return "Є " + str(self.taxes_value).replace(",", ".")

    @property
    def discount_value_str(self):
        return str(self.discount_value).replace(",", ".")

    @property
    def discount_value_money(self):
        return "Є " + str(self.discount_value).replace(",", ".")

    @property
    def total_amount_str(self):
        return str(self.total_amount).replace(",", ".")

    @property
    def total_amount_money(self):
        return "Є " + str(self.total_amount).replace(",", ".")
    
    @property
    def created_at_str(self):
        return self.created_at.strftime(settings.DATETIME_FORMAT_STR)
    
    @property
    def updated_at_str(self):
        return self.updated_at.strftime(settings.DATETIME_FORMAT_STR)
    
    @property
    def status_color(self):
        return {
            'Pendente': '#f9e79f',
            'Pago': '#abebc6',
            'Cancelado': '#f5b7b1',
            'Vencido': '#f9e79f',
        }.get(self.status, '#e5e7e9')


class CustomerInvoice(BaseInvoice):
    
    def __str__(self):
        return f"{self.code} - {self.booking.client_name}"


class PartnerInvoice(BaseInvoice):
    
    def __str__(self):
        return f"{self.code} - {self.booking.partner.name}"
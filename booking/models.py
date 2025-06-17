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
    experience = models.ForeignKey(Experience, on_delete=models.SET_NULL, null=True, db_index=True)
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(WineUser, on_delete=models.SET_NULL, null=True, db_index=True, related_name='bkg_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(WineUser, on_delete=models.SET_NULL, null=True, db_index=True, related_name='bkg_updated_by')

    def __str__(self):
        return f"{self.code} - {self.client_name}"
    
    @property
    def experience_date_str(self):
        return self.experience_date.strftime("%Y-%m-%d")
    
    @property
    def created_at_str(self):
        return self.created_at.strftime("%Y-%m-%d")
    
    @property
    def updated_at_str(self):
        return self.updated_at.strftime("%Y-%m-%d")
    
    @property
    def total_str(self):
        return str(self.total).replace(',', '.')
    
    @property
    def price_adults_str(self):
        return str(self.price_adults).replace(',', '.')
    
    @property
    def price_children_str(self):
        return str(self.price_children).replace(',', '.')
    
    @property
    def discount_str(self):
        return str(self.discount).replace(',', '.')
    

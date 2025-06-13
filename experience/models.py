from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, EmailValidator, URLValidator
# Create your models here.

from django.db import models
from home_auth.models import WineUser

import uuid

class ExperienceStatus(models.TextChoices):
    AVAILABLE = 'Disponível', 'Disponível'
    UNAVAILABLE = 'Indisponível', 'Indisponível'


class ExperienceCategory(models.TextChoices):
    ALMOCOS_DE_DEGUSTACAO = 'Almoços de Degustação', 'Almoços de Degustação'
    CRUZEIROS_DE_2_DIAS = 'Cruzeiros de 2 dias', 'Cruzeiros de 2 dias'
    CRUZEIROS_NO_DOURO = 'Cruzeiros no Douro', 'Cruzeiros no Douro'
    CRUZEIROS_PRIVADOS_E_PREMIUM = 'Cruzeiros Privados e Premium', 'Cruzeiros Privados e Premium'
    CRUZEIROS_TEMATICOS = 'Cruzeiros Temáticos', 'Cruzeiros Temáticos'
    DESPEDIDAS_DE_SOLTEIRO = 'Despedidas de Solteiro', 'Despedidas de Solteiro'
    ESTADIA_E_ESCAPADINHAS = 'Estadia & Escapadinhas', 'Estadia & Escapadinhas'
    EVENTOS_COM_HARMONIZACAO_VINICA = 'Eventos com harmonização vínica', 'Eventos com harmonização vínica'
    EVENTOS_CORPORATIVOS = 'Eventos Corporativos', 'Eventos Corporativos'
    EXPERIENCIAS_PARA_2 = 'Experiências para 2', 'Experiências para 2'
    EXPERIENCIAS_VINICAS = 'Experiências Vínicas', 'Experiências Vínicas'
    FINS_DE_SEMANA_VINICOS = 'Fins-de-semana Vínicos', 'Fins-de-semana Vínicos'
    GASTRONOMIA_E_TRADICAO = 'Gastronomia & Tradição', 'Gastronomia & Tradição'
    GRUPOS_E_EMPRESAS = 'Grupos & Empresas', 'Grupos & Empresas'
    GRUPOS_PRIVADOS = 'Grupos Privados', 'Grupos Privados'
    JANTARES_E_ALMOCOS_VINICOS = 'Jantares e Almoços Vínicos', 'Jantares e Almoços Vínicos'
    JANTARES_TEMATICOS = 'Jantares Temáticos', 'Jantares Temáticos'
    PACKS_ROMANTICOS = 'Packs Românticos', 'Packs Românticos'
    PIQUENIQUES_NAS_VINHAS = 'Piqueniques nas Vinhas', 'Piqueniques nas Vinhas'
    PRESENTES_DE_ULTIMA_HORA = 'Presentes de Última Hora', 'Presentes de Última Hora'
    PRESENTES_E_VOUCHERS = 'Presentes & Vouchers', 'Presentes & Vouchers'
    PROVAS_DE_VINHO = 'Provas de Vinho', 'Provas de Vinho'
    ROTEIROS_PERSONALIZADOS = 'Roteiros Personalizados', 'Roteiros Personalizados'
    SAIDAS_DA_REGUA = 'Saídas da Régua', 'Saídas da Régua'
    SAIDAS_DO_PORTO = 'Saídas do Porto', 'Saídas do Porto'
    SEM_CATEGORIA = 'Sem categoria', 'Sem categoria'
    VINDIMAS_E_EVENTOS_SAZONAIS = 'Vindimas & Eventos Sazonais', 'Vindimas & Eventos Sazonais'
    VISITAS_A_QUINTAS_E_CAVAS = 'Visitas a Quintas e Cavas', 'Visitas a Quintas e Cavas'
    

class Experience(models.Model):
    title = models.CharField(max_length=180, blank=False, null=False)
    # description = models.TextField(blank=False, null=False)
    # departure_place = models.CharField(max_length=255, blank=False, null=False)
    # latitude = models.DecimalField(max_digits=11, decimal_places=9, validators=[MinValueValidator(-90.0, "Valor de latitude não pode ser inferior a -90!"), MaxValueValidator(90.0, "Valor de latitude não pode ser superior a 90!")], blank=True, null=True)
    # longitude = models.DecimalField(max_digits=12, decimal_places=9, validators=[MinValueValidator(-180.0, "Valor de longitude não pode ser inferior a -180!"), MaxValueValidator(180.0, "Valor de longitude não pode ser inferior a -180!")], blank=True, null=True)
    # maps_url = models.URLField(max_length=255, blank=True, null=True, validators=[URLValidator(message="URL inválida! Certifique-se de que a URL está correta.")])
    wordpress_url = models.URLField(max_length=255, blank=True, null=True, validators=[URLValidator(message="URL inválida! Certifique-se de que a URL está correta.")])
    category = models.CharField(max_length=50, choices=ExperienceCategory.choices, default=ExperienceCategory.SEM_CATEGORIA)
    status = models.CharField(max_length=50, choices=ExperienceStatus.choices, default=ExperienceStatus.AVAILABLE)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class RegisterStatus(models.IntegerChoices):
    INACTIVE = 0, 'Inativo'
    ACTIVE = 1, 'Ativo'
    BLOCKED = 2, 'Bloqueado'
    EXCLUDED = 3, 'Excluído'
    

class Partner(models.Model):
    name = models.CharField(max_length=180)
    nif = models.CharField(max_length=15, unique=True, db_index=True)
    iban = models.CharField(max_length=34, unique=True, db_index=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(max_length=255, unique=True, db_index=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=RegisterStatus.choices, default=RegisterStatus.ACTIVE)

    def __str__(self):
        return f"{self.name} - ({self.nif})"


class ReservationChannel(models.IntegerChoices):
    WEBSITE = 0, 'Website'
    WHATSAPP = 1, 'Whatsapp'
    INSTAGRAM = 2, 'Instagram'
    FACEBOOK = 3, 'Facebook'


class ReservationStatus(models.IntegerChoices):
    PENDING = 0, 'Pendente'
    CONFIRMED = 1, 'Confirmada'
    CANCELLED_BY_CLIENT = 2, 'Cancelada (Cliente)'
    CANCELLED_BY_PARTNER = 3, 'Cancelada (Parceiro)'


class Reservation(models.Model):
    reservation_code = models.CharField(max_length=13)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField(max_length=255, db_index=True)
    client_phone = models.CharField(max_length=15)
    reservation_date = models.DateTimeField(auto_now_add=True)
    number_of_adults = models.PositiveIntegerField()
    number_of_children = models.PositiveIntegerField()
    total_adult_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_child_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='reservations_experience')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='reservations_partner')
    reserved_by = models.ForeignKey(WineUser, on_delete=models.CASCADE, related_name='reservations_user')
    channel = models.CharField(max_length=20, choices=ReservationChannel.choices, default=ReservationChannel.WEBSITE)
    status = models.CharField(max_length=30, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)

    def __str__(self):
        return f"Reserva para {self.experience.title}, do cliente {self.client_name} ({self.reservation_code})"


class PaymentMethod(models.IntegerChoices):
    BANK_TRANSFER = 0, 'Referência Multibanco'
    CREDIT_CARD = 1, 'Cartão de Crédito'
    DEBIT_CARD = 2, 'Cartão de Débito'
    MBWAY = 3, 'MB WAY'
    CASH = 4, 'Dinheiro'


class InvoiceStatus(models.IntegerChoices):
    PENDING = 0, 'Pendente'
    PAID = 1, 'Paga'
    CANCELLED = 2, 'Cancelada'
    EXPIRED = 3, 'Expirada'


class CustomerInvoice(models.Model):
    invoice_number = models.CharField(max_length=13)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='invoices_reservation')
    invoice_date = models.DateField(auto_now_add=True)
    emission_date = models.DateField()
    payment_due_date = models.DateField()
    paid_date = models.DateField(null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices, default=PaymentMethod.BANK_TRANSFER)
    status = models.CharField(max_length=30, choices=InvoiceStatus.choices, default=InvoiceStatus.PENDING)

    def __str__(self):
        return f"Fatura Cliente: {self.invoice_number}, {self.reservation.client_name} ({self.reservation.reservation_code})"


class PartnerInvoice(models.Model):
    invoice_number = models.CharField(max_length=13)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='partner_invoices_reservation')
    invoice_date = models.DateField(auto_now_add=True)
    emission_date = models.DateField()
    payment_due_date = models.DateField()
    paid_date = models.DateField(null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices, default=PaymentMethod.BANK_TRANSFER)
    status = models.CharField(max_length=30, choices=InvoiceStatus.choices, default=InvoiceStatus.PENDING)

    def __str__(self):
        return f"Fatura Parceiro: {self.invoice_number}, {self.reservation.partner.name} ({self.reservation.reservation_code})"

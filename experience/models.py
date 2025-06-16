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
    created_by = models.ForeignKey(WineUser, on_delete=models.SET_NULL, null=True, db_index=True, related_name='exp_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(WineUser, on_delete=models.SET_NULL, null=True, db_index=True, related_name='exp_updated_by')
    
    def __str__(self):
        return self.title

class RegisterStatus(models.TextChoices):
    ACTIVE = 'Ativo', 'Ativo'
    BLOCKED = 'Bloqueado', 'Bloqueado'
    EXCLUDED = 'Excluído', 'Excluído'
    INACTIVE = 'Inativo', 'Inativo'
    

class Partner(models.Model):
    name = models.CharField(max_length=180)
    contact_email = models.EmailField(max_length=255, unique=True, db_index=True, validators=[EmailValidator(message="Email inválido! Certifique-se de que o email informado está correto.")])
    contact_phone1 = models.CharField(max_length=15, blank=True, null=True)
    contact_phone2 = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True, validators=[URLValidator(message="URL inválida! Certifique-se de que a URL está correta.")])
    address = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=RegisterStatus.choices, default=RegisterStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(WineUser, on_delete=models.SET_NULL, null=True, db_index=True, related_name='part_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(WineUser, on_delete=models.SET_NULL, null=True, db_index=True, related_name='part_updated_by')

    def __str__(self):
        return self.name

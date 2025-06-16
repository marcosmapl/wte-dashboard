from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone

import uuid

class WineUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    login_token = models.CharField(max_length=6, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Fields for user roles
    is_booking_agent = models.BooleanField(default=False) 
    is_general_manager = models.BooleanField(default=False)
    is_it_manager = models.BooleanField(default=False) 
    is_read_only = models.BooleanField(default=False) 

    # Set related_name to None to prevent reverse relationship creation
    groups = models.ManyToManyField(
        'auth.Group',
        related_name=None,
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name=None,
        blank=True
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name']

    def __str__(self):
        return self.username


class PasswordResetRequest(models.Model):
    user = models.ForeignKey(WineUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    token = models.CharField(max_length=32, default=get_random_string(32), editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Define token validity period (e.g., 1 hour)
    TOKEN_VALIDITY_PERIOD = timezone.timedelta(hours=1)

    def is_valid(self):
        return timezone.now() <= self.created_at + self.TOKEN_VALIDITY_PERIOD

    def send_reset_email(self):
        reset_link = f"http://localhost:8000/authentication/reset-password/{self.token}/"
        send_mail(
            'Password Reset Request',
            f'Click the following link to reset your password: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )
        



        
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   path('', views.dashboard_general, name='dashboard_general'), 
   path('services/', views.dashboard_booking, name='dashboard_booking'), 
]

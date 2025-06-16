from django.urls import path
from . import views

urlpatterns = [
   path('list/', views.list_booking, name='list_booking'),
   path('add/', views.add_booking, name='add_booking'),
   path('edit/<int:id>/', views.edit_booking, name='edit_booking'),
   path('delete/<int:id>/', views.delete_booking, name='delete_booking'),  
]

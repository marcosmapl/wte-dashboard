from django.urls import path
from . import views

urlpatterns = [
   path('list/', views.list_booking_view, name='list_booking'),
   path('add/', views.add_booking_view, name='add_booking'),
   path('edit/<int:id>/', views.edit_booking_view, name='edit_booking'),
   path('delete/<int:id>/', views.delete_booking_view, name='delete_booking'), 
   path('view/<int:id>/', views.view_booking, name='view_booking'), 
]

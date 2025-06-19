from django.urls import path
from . import views

urlpatterns = [
   path('list/', views.list_experience, name='list_experience'),
   path('add/', views.add_experience, name='add_experience'),
   path('edit/<int:id>/', views.edit_experience, name='edit_experience'),
   path('delete/<int:id>/', views.delete_experience, name='delete_experience'),
   path('view/<int:id>/', views.view_experience, name='view_experience'),
   path('partner-list/', views.list_partner, name='list_partner'),
   path('partner-add/', views.add_partner, name='add_partner'),
   path('partner-edit/<int:id>/', views.edit_partner, name='edit_partner'),
   path('partner-delete/<int:id>/', views.delete_partner, name='delete_partner'),
   path('partner-view/<int:id>/', views.view_partner, name='view_partner'),
]

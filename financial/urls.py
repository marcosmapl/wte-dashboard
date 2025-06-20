from django.urls import path
from . import views

urlpatterns = [
   path('list-customer-invoice/', views.list_customer_invoice_view, name='list_customer_invoice'),
   path('add-customer-invoice/', views.add_customer_invoice_view, name='add_customer_invoice'),
   path('edit-customer-invoice/<int:id>/', views.edit_customer_invoice_view, name='edit_customer_invoice'),
   path('delete-customer-invoice/<int:id>/', views.delete_customer_invoice_view, name='delete_customer_invoice'), 
   path('view-customer-invoice/<int:id>/', views.customer_invoice_view, name='view_customer_invoice'), 
   path('list-partner-invoice/', views.list_partner_invoice_view, name='list_partner_invoice'),
   path('add-partner-invoice/', views.add_partner_invoice_view, name='add_partner_invoice'),
   path('edit-partner-invoice/<int:id>/', views.edit_partner_invoice_view, name='edit_partner_invoice'),
   path('delete-partner-invoice/<int:id>/', views.delete_partner_invoice_view, name='delete_partner_invoice'),  
   path('view-partner-invoice/<int:id>/', views.partner_invoice_view, name='view_partner_invoice'), 
]

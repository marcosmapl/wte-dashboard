from django.urls import path
from . import views

urlpatterns = [
   path('list/', views.list_experience, name='list_experience'),
   path('add/', views.add_experience, name='add_experience'),
   path('edit/<int:id>/', views.edit_experience, name='edit_experience'),
   path('delete/<int:id>/', views.delete_experience, name='delete_experience'),
   path('partner-list/', views.list_partner, name='list_partner'),
   path('partner-add/', views.add_partner, name='add_partner'),
   path('partner-edit/<int:id>/', views.edit_partner, name='edit_partner'),
   path('partner-delete/<int:id>/', views.delete_partner, name='delete_partner'),
   # path('detail/<int:id>/', views.detail_experience, name='detail_experience'),
   # path('search/', views.search_experience, name='search_experience'),
   # path('favoritar/<int:id>/', views.favoritar, name='favoritar_experiencia'),
   # path('favoritas/', views.favoritas, name='favoritas_experiencias'),
   # path('favoritas/remover/<int:id>/', views.remover_favorita, name='remover_favorita' ),
   # path('favoritas/limpar/', views.limpar_favoritas, name='limpar_favoritas' ),
   # path('favoritas/compartilhar/<int:id>/', views.compartilhar_favorita, name='compartilhar_favorita' ),
   # path('favoritas/compartilhar/', views.compartilhar_favoritas, name='compartilhar_favoritas' ),
   # path('favoritas/compartilhar/confirmar/', views.confirmar_compartilhamento, name='confirmar_compartilhamento' ),
   # path('favoritas/compartilhar/confirmar/<int:id>/', views.confirmar_compartilhamento, name='confirmar_compartilhamento_id' ),
   # path('favoritas/compartilhar/confirmar/<int:id>/<str:email>/', views.confirmar_compartilhamento, name='confirmar_compartilhamento_email' ),
   # path('favoritas/compartilhar/confirmar/<int:id>/<str:email>/<str:token>/', views.confirmar_compartilhamento, name='confirmar_compartilhamento_token' ),   
]

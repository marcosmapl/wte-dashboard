from django.shortcuts import render

# Create your views here.
def experience_list(request):
    return render(request, "experience/listar_experiencias.html")
              
def add_experience(request):
    pass
              
def edit_experience(request, id):
    pass

def delete_experience(request, id):
    pass

def detail_experience(request, id):
    pass

def search_experience(request):
    pass

# path('nova/', views.insert, name='nova_experiencia'),
# path('listar/', views.listar, name='listar_experiencias'),
# path('editar/<int:id>/', views.editar, name='editar_experiencia'),
# path('deletar/<int:id>/', views.deletar, name='deletar_experiencia'),
# path('detalhes/<int:id>/', views.detalhes, name='detalhes_experiencia'),
# path('buscar/', views.buscar, name='buscar_experiencia'),
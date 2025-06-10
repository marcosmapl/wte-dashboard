from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages

# from .forms import ExperienceForm
from .models import Experience, ExperienceStatus, ExperienceCategory

# Create your views here.
def experience_list(request):
    experience_list = Experience.objects.all().order_by('-created_at')
    return render(request, "experience/list-experience.html", {'experience_list': experience_list})
              
def add_experience(request):
    print("Adicionando nova experiência")

    context = {
        'category_options': ExperienceCategory.choices,
        'status_options': ExperienceStatus.choices,
        'category_selected': ExperienceCategory.SEM_CATEGORIA,
        'status_selected': ExperienceStatus.AVAILABLE,
    }

    if request.method == "POST":
        print(f"Request POST data: {request.POST}")
        
        title = request.POST.get('title')
        # description = request.POST.get('description')
        departure_place = request.POST.get('departure_place')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        maps_url = request.POST.get('maps_url')
        category = request.POST.get('category')
        status = ExperienceStatus.AVAILABLE
        notes = request.POST.get('notes')
        print("Dados recebidos:")
        
        # Criação do objeto
        experience = Experience(
            title=title,
            # description=description,
            departure_place=departure_place,
            latitude=latitude,
            longitude=longitude,
            maps_url=maps_url,
            category=category,
            status=status,
            notes=notes
        )
        
        try:
            # Validação do objeto
            experience.full_clean()
            print("Objeto validado com sucesso")
            
            # Salva o objeto no banco de dados
            experience.save()
            print("Objeto salvo com sucesso")
            
            #TODO: show message popup
            messages.success(request, "Experiência adicionada com sucesso.")
            return redirect('list_experience')
        except ValidationError as e:
            messages.error(request, "Erro de validação: verifique os dados informados.")
            context['errors'] = e.message_dict
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
            context['errors'] = e.message_dict
            # Preenche os campos do contexto para manter os valores
            context.update({
                'form_data': request.POST,
                'category_selected': category,
                'status_selected': status,
            })

    # Renderiza o template com o contexto
    # TODO: add error message popup
    return render(request, "experience/add-experience.html", context)
              
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
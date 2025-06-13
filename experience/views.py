from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages

from django.shortcuts import get_object_or_404

# from .forms import ExperienceForm
from .models import Experience, ExperienceStatus, ExperienceCategory

# Create your views here.
def experience_list(request):
    experience_list = Experience.objects.all().order_by('title').values()
    print(f"Experience list: {experience_list}")
    context = {
        'page_mode': 'list',
        'experience_list': experience_list,
    }
    return render(request, "experience/list-experience.html", context)
         
              
def add_experience(request):
    context = {
        'page_mode': 'add',
        'category_options': ExperienceCategory.choices,
        'status_options': ExperienceStatus.choices,
    }

    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")

        # Criação do objeto
        experience = Experience(
            title=request.POST.get('title'),
            # description=request.POST.get('description'),
            # departure_place=request.POST.get('departure_place'),
            # latitude=request.POST.get('latitude'),
            # longitude=request.POST.get('longitude'),
            # maps_url=request.POST.get('maps_url'),
            wordpress_url=request.POST.get('wordpress_url'),
            category=request.POST.get('category', ExperienceCategory.SEM_CATEGORIA),
            status=request.POST.get('status', ExperienceStatus.AVAILABLE),
            notes=request.POST.get('notes')
        )
        
        try:
            # Validação do objeto
            experience.full_clean()
            
            # Salva o objeto no banco de dados
            experience.save()
            
            #TODO: show message popup
            messages.success(request, "Experiência adicionada com sucesso.")
            return redirect('list_experience')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                messages.error(request, f"Erro de validação: {".".join(errors)}")
                break            
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
            # Preenche os campos do contexto para manter os valores
            context.update({
                'form_data': request.POST,
                'experience': experience,
                'category_selected': experience.category,
                'status_selected': experience.status,
            })

    # Renderiza o template com o contexto
    # TODO: add error message popup
    return render(request, "experience/add-experience.html", context)
              
def edit_experience(request, id):
    experience = Experience.objects.get(id=id)
    
    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")

        # Atualiza os campos do objeto
        experience.title = request.POST.get('title')
        # experience.description = request.POST.get('description')
        # experience.departure_place = request.POST.get('departure_place')
        # experience.latitude = request.POST.get('latitude')
        # experience.longitude = request.POST.get('longitude')
        # experience.maps_url = request.POST.get('maps_url')
        experience.wordpress_url = request.POST.get('wordpress_url')
        experience.category = request.POST.get('category')
        experience.status = request.POST.get('status')
        experience.notes = request.POST.get('notes')
        experience.modified_at = None # Reseta o campo modified_at para que seja atualizado no save()
        
        try:
            # Validação do objeto
            experience.full_clean()
            
            # Salva o objeto no banco de dados
            experience.save()
            
            messages.success(request, "Experiência editada com sucesso.")
            return redirect('list_experience')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                messages.error(request, f"Erro de validação: {".".join(errors)}")
                break            
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
    
    print(f"Experience details: {experience.category}, {experience.status}")
    
    context = {
        'page_mode': 'edit',
        'experience': experience,
        'category_options': ExperienceCategory.choices,
        'category_selected': str(experience.category),
        'status_options': ExperienceStatus.choices,
        'status_selected': str(experience.status),
    }
    
    return render(request, "experience/edit-experience.html", context)

def delete_experience(request, id):
    if request.method == "POST":
        experience = get_object_or_404(Experience, id=id)
        # Verifica se o objeto existe
        if not experience:
            messages.error(request, "Experiência não encontrada.")
        else:
            # Exclui o objeto
            messages.success(request, "Experiência excluída com sucesso.")    
            experience.delete()
    
    return redirect('list_experience')


def search_experience(request):
    pass

# path('nova/', views.insert, name='nova_experiencia'),
# path('listar/', views.listar, name='listar_experiencias'),
# path('editar/<int:id>/', views.editar, name='editar_experiencia'),
# path('deletar/<int:id>/', views.deletar, name='deletar_experiencia'),
# path('detalhes/<int:id>/', views.detalhes, name='detalhes_experiencia'),
# path('buscar/', views.buscar, name='buscar_experiencia'),
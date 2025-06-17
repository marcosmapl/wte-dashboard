from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages

from django.shortcuts import get_object_or_404

from home_auth.models import WineUser

# from .forms import ExperienceForm
from .models import Experience, ExperienceStatus, ExperienceCategory, Partner, RegisterStatus

# EXPERIENCE VIEWS
def list_experience(request):
    experience_list = Experience.objects.all().order_by('title').values()
    # print(f"Experience list: {experience_list}")
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
            notes=request.POST.get('notes'),
            created_by=request.user,
            updated_by=request.user
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
                print(field, errors)
                messages.error(request, f"Erro de validação: {".".join(errors)}")
                break            
        except Exception as e:
            print(e)
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
    experience = Experience.objects.select_related('created_by', 'updated_by').get(id=id)
    
    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")

        # Atualiza os campos do objeto
        experience.title = request.POST.get('title')
        experience.wordpress_url = request.POST.get('wordpress_url')
        experience.category = request.POST.get('category')
        experience.status = request.POST.get('status')
        experience.notes = request.POST.get('notes')
        experience.updated_by = request.user
        experience.updated_at = None # Reseta o campo modified_at para que seja atualizado no save()
        
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
    
    # print(f"Experience details: {experience.category}, {experience.status}")
    
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


# PARTNER VIEWS
def list_partner(request):
    partner_list = Partner.objects.all().order_by('name').values()
    # print(f"Partner list: {partner_list}")
    context = {
        'page_mode': 'list',
        'partner_list': partner_list,
    }
    return render(request, "experience/list-partner.html", context)
       
              
def add_partner(request):
    context = {
        'page_mode': 'add',
        'status_options': RegisterStatus.choices,
    }

    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")

        # Criação do objeto
        partner = Partner(
            name=request.POST.get('name'),
            contact_email=request.POST.get('contact_email'),
            contact_phone1=request.POST.get('contact_phone1'),
            contact_phone2=request.POST.get('contact_phone2'),
            website=request.POST.get('website'),
            address=request.POST.get('address'),
            status=request.POST.get('status', RegisterStatus.ACTIVE),
            created_by=request.user,
            updated_by=request.user,
        )
        
        try:
            # Validação do objeto
            partner.full_clean()
            
            # Salva o objeto no banco de dados
            partner.save()
            
            #TODO: show message popup
            messages.success(request, "Parceiro adicionada com sucesso.")
            return redirect('list_partner')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                messages.error(request, f"Erro de validação: {".".join(errors)}")
                break            
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
            # Preenche os campos do contexto para manter os valores
            context.update({
                'form_data': request.POST,
                'partner': partner,
                'status_selected': partner.status,
            })

    # Renderiza o template com o contexto
    # TODO: add error message popup
    return render(request, "experience/add-partner.html", context)


def edit_partner(request, id):
    partner = Partner.objects.get(id=id)
    
    if request.method == "POST":
        # print(f"Request POST data: {request.POST}")

        # Atualiza os campos do objeto
        partner.name = request.POST.get('name')
        partner.contact_email = request.POST.get('contact_email')
        partner.contact_phone1 = request.POST.get('contact_phone1')
        partner.contact_phone2 = request.POST.get('contact_phone2')
        partner.website = request.POST.get('website')
        partner.status = request.POST.get('status')
        partner.address = request.POST.get('address')
        partner.updated_by = request.user
        partner.updated_at = None # Reseta o campo modified_at para que seja atualizado no save()
        
        try:
            # Validação do objeto
            partner.full_clean()
            
            # Salva o objeto no banco de dados
            partner.save()
            
            messages.success(request, "Parceiro editado com sucesso.")
            return redirect('list_partner')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                messages.error(request, f"Erro de validação: {".".join(errors)}")
                break            
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
    
    context = {
        'page_mode': 'edit',
        'partner': partner,
        'status_options': RegisterStatus.choices,
        'status_selected': str(partner.status),
    }
    
    return render(request, "experience/edit-partner.html", context)


def delete_partner(request, id):
    if request.method == "POST":
        partner = get_object_or_404(Partner, id=id)
        
        # Verifica se o objeto existe
        if not partner:
            messages.error(request, "Parceiro não encontrado.")
        else:
            # Exclui o objeto
            messages.success(request, "Parceiro excluído com sucesso.")    
            partner.delete()
    
    return redirect('list_partner')
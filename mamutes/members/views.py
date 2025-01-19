
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .forms import TaskForm
from .models import MembroEquipe, Task,Area

from rest_framework import viewsets
from .models import Column, Task
from .serializers import ColumnSerializer, TaskSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date, datetime

import locale

import base64

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


def sidebar(request):
     members = MembroEquipe.objects.all()
     return render(request,"partials/_sidebar.html", {'members':members})

def Top(request):
     return render(request, 'partials/Top.html')

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid(): 
         task = form.save()  # Salva a tarefa
                 # Salva os relacionamentos ManyToMany
    else:
            form = TaskForm()


def delete_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('id_task')
                
        if task_id:
            task = get_object_or_404(Task, id=task_id)
            task.delete()  # Deleta a task
        return redirect('kanban')

    return redirect('kanban')

def edit_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('id_task')
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        prazo = request.POST.get('Prazo')
        print('CAIO FERREIRA DUARTE')
        print(task_id,title,description,status,prazo)

        print('AAAAAAAAAAAAAAAAAAAAAAAA')
        if task_id:
            task = get_object_or_404(Task, id=task_id)
            if title:
                task.title = title
            if description:
                task.description = description
            if status:
                task.priority = priority
            if prazo:
                task.Prazo = prazo
            task.save()

        return redirect('kanban')

    return redirect('kanban')

class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        column_id = self.request.query_params.get('column')
        if column_id:
            return self.queryset.filter(column_id=column_id)
        return self.queryset


def kanban_view(request):
    # Obtém a área a partir dos parâmetros da URL (GET)
    area_id = request.GET.get('area')  # Exemplo: ?area=SE
    
    # Filtra as tarefas pela área, se especificada
    if area_id:
        # Filtra as tarefas pela área especificada na URL
        tasks = Task.objects.filter(area__id=area_id)
    else:
        # Caso nenhuma área seja especificada, exibe todas as tarefas
        tasks = Task.objects.all()  # Caso nenhuma área seja especificada, retorna todas as tarefas
    
    items = []
    profiles = MembroEquipe.objects.all()
    members = []
    
    all_areas = Area.objects.all()
    # Processa os membros da equipe
    for profile in profiles:
        if profile.photo:
            profile.photo_base64 = base64.b64encode(profile.photo).decode('utf-8')
        
        members.append({
            'email': profile.email,
            'fullname': profile.fullname,
            'username': profile.username,
            'photo': profile.photo,
        })
    total_tasks = tasks.count()
    completed_task_count = tasks.filter(status='Concluída').count()
    Em_Progresso_task_count = tasks.filter(status='Em Progresso').count()
    Pendente_count = tasks.filter(status='Pendente').count()
    
    if total_tasks > 0:
        pending_percentage = round((Pendente_count / total_tasks) * 100)
        in_progress_percentage = round((Em_Progresso_task_count / total_tasks) * 100)
        completed_percentage = round((completed_task_count / total_tasks) * 100)
    else:
        pending_percentage = in_progress_percentage = completed_percentage = 0
    # Processa as tarefas
    for task in tasks:
        prazo = task.Prazo
        today = datetime.now().date()
        if prazo:
            if prazo == today:
                formatted_date = "HOJE"
            else:
                formatted_date = prazo.strftime("%d / %m / %Y")
        else:
            formatted_date = "Sem prazo definido"

        responsible_profiles = task.responsible.all()
        responsible_photos = []
        
        for resp in responsible_profiles:
            if resp.photo:
                responsible_photos.append(base64.b64encode(resp.photo).decode('utf-8'))
            else:
                responsible_photos.append(None)
        
        pair_r_p = list(zip(task.get_responsibles(), responsible_photos))
        items.append({
            'id': task.id,
            'status': task.status,
            'title': task.title,
            'description': task.description,
            'creation_date': task.creation_date,
            'priority': task.priority,
            'prazo': formatted_date,
            'completion_date': task.completion_date,
            'responsible': task.get_responsibles_as_string(),
            'responsible_photos': responsible_photos,
            'responsible_count': task.responsible.count(),
            'pair_responsible_photo': pair_r_p,
        })
    
    # Adicionar nova tarefa via POST
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        prazo = request.POST.get('Prazo') or None
        responsible = request.POST.get('responsibles')
        
        responsible = list(map(int, responsible.split(',')))

        # Cria a instância de Task
        task = Task.objects.create(
            title=title,
            description=description,
            status=status,
            priority=priority,
            Prazo=prazo,
        )

        responsible_members = MembroEquipe.objects.filter(id__in=responsible)
        task.responsible.set(responsible_members)
        
        return redirect('kanban')
    
    return render(request, 'kanbam.html', {
        'items': items,
        'profiles': profiles,
        'members': members,
        'selected_area': area_id,
        'all_areas': all_areas,
        'completed_task_count': completed_task_count,
        'Em_Progresso_task_count': Em_Progresso_task_count,
        'Pendente_count':  Pendente_count,
        'pending_percentage': pending_percentage,
        'in_progress_percentage': in_progress_percentage,
        'completed_percentage': completed_percentage,
    })



@api_view(['PATCH'])
def update_task_status(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Log os dados recebidos
    print("Dados recebidos:", request.data)

    new_status = request.data.get('status')
    if not new_status:
        return Response({"error": "Status not provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    task.status = new_status
    task.save()

    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)

    
def upload_photo(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        email = request.POST['email']
        phone = request.POST['phone']
        photo = request.FILES['photo']  # Obtém o arquivo enviado
        photo_data = photo.read()  # Lê os dados binários do arquivo

        # Salva no banco
        profile = MembroEquipe(fullname=fullname, photo=photo_data,email=email,phone=phone,username=fullname)
        profile.save()

        return redirect('profile_list')  # Redireciona para outra página
    return render(request, 'upload_photo.html')

def profile_list(request):
    profiles = MembroEquipe.objects.all()
    for profile in profiles:
        # Converte o blob em uma string Base64
        if profile.photo:
            profile.photo_base64 = base64.b64encode(profile.photo).decode('utf-8')
    return render(request, 'profile_list.html', {'profiles': profiles})

@login_required
def home(request):
    return render(request, "home.html")


import profile
from django.http import JsonResponse
import base64
from django.shortcuts import render, redirect, get_object_or_404

from .models import AccidentLog, FlightLog,Meeting,Area,MembroEquipe
from .forms import FlightForm,MeetingsForm
from django.contrib.auth.decorators import login_required

# Listar todos os voos
def flight_list(request):
    flight = FlightLog.objects.all()
    return render(request, 'report/flight_list.html', {'flights': flight})

# Criar um novo voo
# def flight_create(request):
#     if request.method == 'POST':
#         form = FlightForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('flights')
#     else:
#         form = FlightForm()
#     return redirect('flights')
from django.shortcuts import render, redirect
from .models import FlightLog

def flight_create(request):
    if request.method == 'POST':
        # Capturando os dados diretamente do request.POST
        flight_log = FlightLog(
            title=request.POST.get('title'),
            date=request.POST.get('date'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            location=request.POST.get('location'),
            flight_success_rating=request.POST.get('flight_success_rating'),
            flight_objective_description=request.POST.get('flight_objective_description'),
            results=request.POST.get('results'),
            pilot_impressions=request.POST.get('pilot_impressions'),
            improvements=request.POST.get('improvements'),
            wind_speed=request.POST.get('wind_speed'),
            wind_direction=request.POST.get('wind_direction'),
            atmospheric_pressure=request.POST.get('atmospheric_pressure'),
            total_takeoff_weight=request.POST.get('total_takeoff_weight'),
            flight_cycles=request.POST.get('flight_cycles'),
            telemetry_link=request.POST.get('telemetry_link'),
            occurred_accident=request.POST.get('occurred_accident', False)  # Valor default False
        )
        flight_log.save()

        # Adicionando relacionamentos ManyToMany (pilots e team_members)
        pilots = request.POST.getlist('pilots')  # Lista de IDs
        team_members = request.POST.getlist('team_members')  # Lista de IDs
        
        if pilots:
            flight_log.pilot_name.set(pilots)  # Define os pilotos relacionados
        if team_members:
            flight_log.team_members.set(team_members)  # Define os membros relacionados
        
        return redirect('flights')
    else:
        # Renderize o formulário vazio caso não seja uma requisição POST
        return render(request, 'flight_create.html')

# Editar um voo existente
def flight_edit(request, id):
    flight = get_object_or_404(FlightLog, id=id)
    if request.method == 'POST':
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            return redirect('flight_list')
    else:
        form = FlightForm(instance=flight)
    return render(request, 'report/flight_form.html', {'form': form})

# Deletar um voo
def flight_delete(request, id):
    flight = get_object_or_404(FlightLog, id=id)
    if request.method == 'POST':
        flight.delete()
        return redirect('flights')
    return redirect('flights')

def image_to_base64(image):
    """
    Converte a imagem do campo ImageField para uma string base64.
    Lida tanto com arquivos de imagem quanto com dados binários.
    """
    if isinstance(image, bytes):  # Se image já for um objeto de bytes
        return base64.b64encode(image).decode('utf-8')
    
    if image:
        with open(image.path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
@login_required
def meetings(request):
    profiles = MembroEquipe.objects.all()
    meetings = Meeting.objects.all()
    items = []

    order = request.GET.get("order", "recentes")
    if order == "recentes":
        meetings = meetings.order_by("-meeting_date") 
    elif order == "antigos":
        meetings = meetings.order_by("meeting_date")

    areas = Area.objects.all()
    areas_select = request.GET.getlist("areas", [])

    if areas_select:
        meetings = meetings.filter(areas__id__in=areas_select).distinct()

    for meeting in meetings:
        responsible_profiles = meeting.responsible.all()
        responsible_photos = []
        
        for resp in responsible_profiles:
            if resp.photo:
                responsible_photos.append(image_to_base64(resp.photo))
            else:
                responsible_photos.append(None)
        pair_r_p = list(zip(meeting.get_responsibles(), responsible_photos))
        meeting.responsibles_list = pair_r_p

    print(meetings)

    for profile in profiles:
            if profile.photo:
                profile.photo_base64 = image_to_base64(profile.photo)
            else:  
                profile.photo_base64 = None
    if request.method == 'POST':
        post_data = request.POST.copy()  # Cria uma cópia dos dados para modificar

        # Converter os IDs de "responsibles" para uma lista
        responsibles_ids = post_data.get("responsibles", "")
        if responsibles_ids:  # Se não estiver vazio
            post_data.setlist("responsible", responsibles_ids.split(","))  # Ajusta para ManyToManyField

        # Converter os IDs de "areas" para lista (caso já existisse no código)
        post_data.setlist("areas", post_data.get("areas", "").split(","))

        # Criar e validar o formulário
        form = MeetingsForm(post_data)
        print(form.is_valid())

        if form.is_valid():
            meeting = form.save(commit=False)  # Salva sem ManyToMany
            meeting.save()  # Primeiro salva a instância

            # Adiciona os relacionamentos ManyToMany manualmente
            meeting.responsible.set(post_data.getlist("responsible"))  
            meeting.areas.set(post_data.getlist("areas"))

            return redirect('meetingsquadro')
    else:
        form = MeetingsForm()
    
    return render(request, 'meetings.html',
    {'form': form,
     'items': items,
     'meetings': meetings,
     "areas": areas,
     "areas_select": areas_select,
     "order": order,
     "profiles": profiles,})

def flights(request):
    flights = FlightLog.objects.all()
    count_flights = FlightLog.objects.all().count()
    count_accidents = FlightLog.objects.filter(occurred_accident = True).count()
    accidents_percentage = count_accidents/count_flights * 100


    profiles = MembroEquipe.objects.all()
    return render(request, 'flights.html', {'flights': flights, 'profiles': profiles, 'count_flights': count_flights, 'count_accidents': count_accidents, 'accidents_percentage':  accidents_percentage})

def membros_por_area(request, area_id):
    """Retorna os membros de uma determinada área."""
    area = get_object_or_404(Area, id=area_id)
    membros = area.membros.all()  # Pega todos os membros que pertencem a essa área
    print("membros:  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print(membros)
    membros_data = [
        {
            "id": membro.id,
            "fullname": membro.fullname,
            "email": membro.email,
            "phone": membro.phone,
            "photo": membro.photo.url if membro.photo else None,
        }
        for membro in membros
    ]

    return JsonResponse({"membros": membros_data})

def delete_meeting(request, meeting_id):
    if request.method == "POST":
        meeting = get_object_or_404(Meeting, id=meeting_id)
        meeting.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)
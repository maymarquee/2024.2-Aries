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


from django.shortcuts import render, redirect
from .models import FlightLog

from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .models import FlightLog, AccidentLog  # Certifique-se de importar os modelos corretos

def flight_create(request):
    if request.method == 'POST':
        occurred_accident = request.POST.get('occurred_accident') == 'on'  # Converte direto para booleano
        print(occurred_accident)

        try:
            # Criando o objeto FlightLog e salvando no banco
            flight_log = FlightLog.objects.create(
                title=request.POST.get('title'),
                date=request.POST.get('date'),
                start_time=request.POST.get('start_time'),
                end_time=request.POST.get('end_time'),
                location=request.POST.get('location'),
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
                occurred_accident=occurred_accident,
                flight_success_rating = request.POST.get('stars'),
            )

            # Adicionando membros da equipe ao FlightLog
            team_members = request.POST.get('responsibles')
            

            if team_members:
                team_members_ids = [int(id.strip()) for id in team_members.split(',') if id.strip().isdigit()]
                flight_log.team_members.set(team_members_ids)  # Define os membros corretamente
            
            print(f"FlightLog criado com ID: {flight_log.id}")

            # Criando log de acidente se necessário
            if occurred_accident:
                AccidentLog.objects.create(
                    id_flightLog=flight_log,
                    description=request.POST.get('descriptionAccident'),
                    damaged_parts=request.POST.get('damaged_parts'),
                    damaged_parts_photo=request.POST.get('damaged_parts_photo')  # Corrigido para usar FILES corretamente
                )

            return redirect('flights')  # Redireciona corretamente

        except Exception as e:
            print(f"Erro ao criar o flight log: {e}")
            return HttpResponseBadRequest("Ocorreu um erro ao criar o log de voo.")

    return render(request, 'flights.html')  # Renderiza a página em caso de GET

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

from django.db.models import Sum
def flights(request):

    flights = FlightLog.objects.all()
    count_flights = FlightLog.objects.all().count()
    count_accidents = FlightLog.objects.filter(occurred_accident = True).count()
    sum_stars = FlightLog.objects.aggregate(Sum('flight_success_rating'))['flight_success_rating__sum']


    if count_flights != 0:
        accidents_percentage = (count_accidents / count_flights) * 100
        accidents_percentage = round(accidents_percentage, 2)
        mid_sucess = sum_stars/count_flights
    else: 
        accidents_percentage = 0
        mid_sucess= 0




    profiles = MembroEquipe.objects.all()

    context = {
        'flights': flights,
        'profiles': profiles,
        'count_flights': count_flights,
        'count_accidents': count_accidents,
        'accidents_percentage':  accidents_percentage,
        'mid_sucess':mid_sucess
    }
    if request.method == 'POST':
        filter_search = request.POST.get('search')
        flights = FlightLog.objects.filter(title__icontains=filter_search)
        context['flights'] = flights
        return render(request, 'flights.html', context)
    return render(request, 'flights.html', context)

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
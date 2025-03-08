from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt



def principal(request):
    return render(request, 'odontologia_app/principal.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')

def inicio_sesion(request):
    if request.method == 'POST':
        email = request.POST.get('email')  
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('principal')  
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')
    return render(request, 'odontologia_app/inicio_sesion.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('principal')  
    else:
        form = RegistroForm()
    return render(request, 'odontologia_app/registro.html', {'form': form})

def inicio(request):
    return render(request, 'odontologia_app/inicio.html')

def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    
    paciente.delete()
    
    return redirect('lista_pacientes')  


def lista_pacientes(request):
    url = 'http://localhost:3000/paciente'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        pacientes = response.json()  
        query = request.GET.get('q')
        
        if query:
            pacientes = [p for p in pacientes if query.lower() in p['nombre'].lower() or query in p['cedula']]
        
        return render(request, 'odontologia_app/lista_pacientes.html', {'pacientes': pacientes})
    else:

        return JsonResponse({'error': 'No se pudieron obtener los pacientes'}, status=500)

def crear_paciente(request):
    if request.method == 'POST':

        datos = {
            'cedula': request.POST.get('cedula'),
            'nombre': request.POST.get('nombre'),  # Nuevo campo "Nombre"
            'cedula_representante': request.POST.get('cedula_representante') or None,
            'edad': int(request.POST.get('edad')),
            'telefono': request.POST.get('telefono'),
            'sexo': request.POST.get('sexo'),
            'estado_civil': request.POST.get('estado_civil') == 'true',
            'ocupacion': request.POST.get('ocupacion'),
        }
        

        url = 'http://localhost:3000/paciente'
        
        response = requests.post(url, json=datos)

        if response.status_code == 201:
            return redirect('lista_pacientes')  
        else:
            print("Error de la API:", response.status_code, response.text)
            return JsonResponse({'error': 'No se pudo crear el paciente'}, status=500)
    else:
        return render(request, 'odontologia_app/crear_paciente.html')
    
 

def editar_paciente(request, id):

    paciente = get_object_or_404(Paciente, id=id)
    
    if request.method == 'POST':
        paciente.cedula = request.POST.get('cedula')
        paciente.nombre = request.POST.get('nombre')
        paciente.cedula_representante = request.POST.get('cedula_representante')
        paciente.edad = int(request.POST.get('edad'))
        paciente.telefono = request.POST.get('telefono')
        paciente.sexo = request.POST.get('sexo')
        paciente.estado_civil = request.POST.get('estado_civil') == 'true'
        paciente.ocupacion = request.POST.get('ocupacion')
        paciente.save()
        

        return redirect('lista_pacientes')
    else:
        return render(request, 'odontologia_app/editar_paciente.html', {'paciente': paciente})
    
def crear_historia_medica(request):
    if request.method == 'POST':
        form = HistoriaMedicaForm(request.POST)
        if form.is_valid():
            historia_medica = form.save(commit=False)
            historia_medica.examinador = request.user  
            historia_medica.save()  
            return redirect('crear_anamnesis', historia_id=historia_medica.id)  
    else:
        form = HistoriaMedicaForm()
    return render(request, 'odontologia_app/crear_historia_medica.html', {'form': form})

def crear_anamnesis(request, historia_id):
    historia_medica = get_object_or_404(Historia_Medica, id=historia_id)
    
    if request.method == 'POST':
        form = AnamnesisForm(request.POST)
        if form.is_valid():
            anamnesis = form.save(commit=False)
            anamnesis.historia_medica = historia_medica  # Asignar la historia médica recién creada
            anamnesis.save()
            return redirect('completar_anamnesis', anamnesis_id=anamnesis.id)  # Redirigir a la lista de historias médicas
    else:
        form = AnamnesisForm()
    return render(request, 'odontologia_app/crear_anamnesis.html', {'form': form, 'historia_medica': historia_medica})

def completar_anamnesis(request, anamnesis_id):
    anamnesis = get_object_or_404(Anamnesis, id=anamnesis_id)
    
    if request.method == 'POST':
        habitos_form = HabitosForm(request.POST)
        antecedentes_form = AntecedentesFamiliaresForm(request.POST)

        if habitos_form.is_valid() and antecedentes_form.is_valid():
            habito = habitos_form.save(commit=False)
            habito.anamnesis = anamnesis
            habito.save()

            antecedente = antecedentes_form.save(commit=False)
            antecedente.anamnesis = anamnesis
            antecedente.save()

            messages.success(request, 'Los hábitos y antecedentes se han guardado correctamente.')
            return redirect('lista_historias_medicas')
    else:
        habitos_form = HabitosForm()
        antecedentes_form = AntecedentesFamiliaresForm()

    return render(request, 'odontologia_app/completar_anamnesis.html', {
        'habitos_form': habitos_form,
        'antecedentes_form': antecedentes_form,
        'anamnesis': anamnesis,
    })

def lista_historias_medicas(request):
    historias = Historia_Medica.objects.filter(examinador=request.user).select_related(
        'anamnesis'
    ).prefetch_related(
        'anamnesis__habitos',  
        'anamnesis__antecedentes_familiares'  
    )
    return render(request, 'odontologia_app/lista_historias_medicas.html', {'historias': historias})
def editar_historia_medica(request, historia_id):

    historia = get_object_or_404(Historia_Medica, id=historia_id)
    
    anamnesis = historia.anamnesis
    habitos = anamnesis.habitos.first()  
    antecedentes = anamnesis.antecedentes_familiares.first()  

    if request.method == 'POST':

        historia_form = HistoriaMedicaForm(request.POST, instance=historia)
        anamnesis_form = AnamnesisForm(request.POST, instance=anamnesis)
        habitos_form = HabitosForm(request.POST, instance=habitos)
        antecedentes_form = AntecedentesFamiliaresForm(request.POST, instance=antecedentes)

        if all([
            historia_form.is_valid(),
            anamnesis_form.is_valid(),
            habitos_form.is_valid(),
            antecedentes_form.is_valid()
        ]):

            historia_form.save()
            anamnesis_form.save()
            habitos_form.save()
            antecedentes_form.save()


            messages.success(request, 'La historia médica se ha actualizado correctamente.')
            return redirect('lista_historias_medicas')
    else:

        historia_form = HistoriaMedicaForm(instance=historia)
        anamnesis_form = AnamnesisForm(instance=anamnesis)
        habitos_form = HabitosForm(instance=habitos)
        antecedentes_form = AntecedentesFamiliaresForm(instance=antecedentes)

    return render(request, 'odontologia_app/editar_historia_medica.html', {
        'historia_form': historia_form,
        'anamnesis_form': anamnesis_form,
        'habitos_form': habitos_form,
        'antecedentes_form': antecedentes_form,
    })

def eliminar_historia_medica(request, historia_id):
    historia = get_object_or_404(Historia_Medica, id=historia_id)
    historia.delete()
    return redirect('lista_historias_medicas')

def crear_representante(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        nombre = request.POST.get('nombre')

        representante = Representante(cedula=cedula, nombre=nombre)
        representante.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
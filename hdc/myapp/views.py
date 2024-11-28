from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from myapp.forms import CustomUserCreationForm, FormCalculadora
from myapp.models import Huella
from django.contrib import messages
import folium

# Vista para la página de inicio
def home(request):
    return render(request, 'myapp/home.html')

# Vista para los productos (puedes cambiarla según lo que necesites)
@login_required
def products(request):
    return render(request, 'myapp/products.html')

# Vista para cerrar sesión
def exit(request):
    logout(request)
    return redirect('home')

# Vista para el registro de usuarios
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password1']
            )
            if user:
                login(request, user)
                messages.success(request, "¡Registro exitoso! Bienvenido.")
                return redirect('home')
            else:
                messages.error(request, "Hubo un problema al autenticar al usuario.")
        else:
            messages.error(request, "El registro falló. Por favor corrige los errores.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

# Vista para la calculadora de huella de carbono
@login_required
def huella(request):
    if request.method == 'POST':
        form = FormCalculadora(request.POST)
        if form.is_valid():
            huella_obj = form.save(commit=False)
            huella_obj.user = request.user  # Asociamos la huella con el usuario actual
            huella_obj.save()  # Guardamos en la base de datos
            
            co2_emisiones = huella_obj.calcular_huella()  # Calculamos las emisiones
            return render(request, 'myapp/huella_result.html', {'co2_emisiones': co2_emisiones, 'huella': huella_obj})
    else:
        form = FormCalculadora()

    return render(request, 'myapp/huella.html', {'form': form})

# Vista para la página "Nosotros" o Preguntas Frecuentes
def nosotros(request):
    return render(request, 'myapp/nosotros.html')

# Vista para el perfil del usuario
@login_required
def perfil(request):
    # Obtenemos todas las huellas de carbono asociadas al usuario
    huellas = Huella.objects.filter(user=request.user)
    return render(request, 'myapp/perfil.html', {'huellas': huellas})

# Vista para el mapa
def mapa(request):
    # Creación del mapa con Folium
    initialMap = folium.Map(location=[-33.490766218519475, -70.61888767914276], zoom_start=18)
    edificios_geojson = {
        "type": "FeatureCollection",
        "features": [
            # Definir los edificios aquí
            {
                "type": "Feature",
                "properties": {"name": "Edificio A", "info": "Información sobre el edificio A"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-70.61834824390719, -33.490502590681416],
                        [-70.61834672131202, -33.49054454440232],
                        [-70.61857546068886, -33.490584336585506],
                        [-70.61840016778497, -33.491342411798],
                        [-70.61848732403907, -33.49135680393925],
                        [-70.61865903830318, -33.490616582621904],
                        [-70.6187831156597, -33.49063393665665],
                        [-70.6185752589204, -33.49150124056633],
                        [-70.61816130514129, -33.4914377933369],
                        [-70.61813918692567, -33.49152281905175],
                        [-70.61797572031787, -33.49149761689295],
                        [-70.6182050014158, -33.49047449981421],
                        [-70.61834824390719, -33.490502590681416]
                    ]]
                }
            },
            # Agregar más edificios si es necesario
        ]
    }

    # Funciones de estilo para los edificios en el mapa
    def style_function(feature):
        return {
            "fillColor": "yellow",
            "color": "black",
            "fillOpacity": 0.2,
            "weight": 1
        }
        
    def highlight_function(feature):
        return {
            "fillColor": "yellow",
            "color": "yellow",
            "fillOpacity": 0.6,
            "weight": 2
        }
    
    # Agregar el GeoJSON al mapa
    folium.GeoJson(
        data=edificios_geojson,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["name"],
            aliases=["Edificio:"],
            localize=True
        ),
        popup=folium.GeoJsonPopup(
            fields=["info"],
            aliases=["Información:"],
            localize=True
        )
    ).add_to(initialMap)
    
    # Pasar el mapa al contexto para renderizarlo
    context = {"mapa": initialMap._repr_html_()}
    
    return render(request, 'mapa/maph.html', context)

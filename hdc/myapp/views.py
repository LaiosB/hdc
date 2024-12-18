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
            huella_obj.co2_emisiones= huella_obj.calcular_huella()  # Calculamos las emisiones
            huella_obj.save()  # Guardamos en la base de datos
            co2_emisiones = huella_obj.co2_emisiones
            
            return redirect('perfil')
    else:
        form = FormCalculadora()

    return render(request,'myapp/huella.html', {'form': form})

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
            {
                "type": "Feature",
                "properties": {"name": "El edificio A posee 3 departamentos esenciales", "info": "El edificio A emite 23.295,6 toneladas de co2 al año"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-70.61834824390719,-33.490502590681416],
                        [-70.61834672131202,-33.49054454440232],
                        [-70.61857546068886,-33.490584336585506],
                        [-70.61840016778497,-33.491342411798],
                        [-70.61848732403907,-33.49135680393925],
                        [-70.61865903830318,-33.490616582621904],
                        [-70.6187831156597,-33.49063393665665],
                        [-70.6185752589204,-33.49150124056633],
                        [-70.61816130514129,-33.4914377933369],
                        [-70.61813918692567,-33.49152281905175],
                        [-70.61797572031787,-33.49149761689295],
                        [-70.6182050014158,-33.49047449981421],
                        [-70.61834824390719,-33.490502590681416]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "El edificio B posee 3 departamentos esenciales", "info": "El edificio B emite 28.922,8 Toneladas de co2 al año."},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-70.62011859544695,-33.49040378567553],
                        [-70.61921392694627,-33.49024656555172],
                        [-70.61930408045005,-33.489779321937405],
                        [-70.61908832079655,-33.48975779910072],
                        [-70.61908324370414,-33.48975294898268],
                        [-70.61911271548523,-33.4896289645344],
                        [-70.62025070645923,-33.48980291040082],
                        [-70.62011859544695,-33.49040378567553]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "El edificio C posee 1 departamento esencial.", "info": "El edificio C emite 8.950,5 toneladas de co2 al año."},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-70.61903159723903,-33.4907391677371],
                        [-70.61893144000994,-33.49119055222705],
                        [-70.61870252788715,-33.49114612017024],
                        [-70.61882028012369,-33.49069968511385],
                        [-70.61903159723903,-33.4907391677371]
                    ]]
                }
                
            },
            {
                "type": "Feature",
                "properties": {"name": "El edificio E posee 1 departamento esencial.", "info": "El edificio E emite 9.013,5 toneladas de co2 al año"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-70.62043352828836,-33.49049909348461],
                        [-70.62025170763883,-33.49050729812055],
                        [-70.6202419812403,-33.490416440207376],
                        [-70.62034211730149,-33.489986162698415],
                        [-70.62021595782652,-33.48996153796307],
                        [-70.62022017592463,-33.48994426866354],
                        [-70.6205070065842,-33.48999095972446],
                        [-70.62042164092105,-33.49039739708091],
                        [-70.62043352828836,-33.49049909348461]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "El edificio F posee 0 departamentos esenciales.", "info": "El edificio F no emite co2 en base a nuestro modelo generalizado."},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-70.61986860475409,-33.49042323769022],
                        [-70.61979967421722,-33.49074803791788],
                        [-70.61840182110004,-33.490535240541064],
                        [-70.6184094365276,-33.49049331202385],
                        [-70.61825382583775,-33.490467979707304],
                        [-70.61832306423271,-33.49016678833369],
                        [-70.61986860475409,-33.49042323769022]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "El edificio K posee 3 departamentos esenciales.", "info": "El edificio K emite 24.983,5 toneladas de co2 al año."},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-70.61972825543411,-33.491422841877],
                        [-70.6196636639087,-33.491689783829884],
                        [-70.61893394826683,-33.49171893630827],
                        [-70.61860237843827,-33.49169499536698],
                        [-70.61838765664487,-33.4916655460946],
                        [-70.61840511941526,-33.49152022629975],
                        [-70.61861673210997,-33.49154895548587],
                        [-70.61870557301017,-33.49126387399327],
                        [-70.61972825543411,-33.491422841877]
                    ]]
                }
            }
        ]
    }
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
        

    context = {"mapa": initialMap._repr_html_()}
    
    return render (request, 'mapa/maph.html', context)
    
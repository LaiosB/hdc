from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from. models import Huella


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model= User
        fields=['username', 'first_name', 'last_name', 'email','password1', 'password2']

class FormCalculadora(forms.ModelForm):
    class Meta:
        model= Huella
        fields= ['transporte','distancia','energia','dieta']

        #REVISAR Y ENTENDER CODIGO
        widgets = {
            'dieta': forms.RadioSelect(),  # Alternativa tipo radio button para dieta
            'transporte': forms.RadioSelect(),  # Alternativa tipo radio button para transporte
            'distancia': forms.NumberInput(attrs={'placeholder': 'Ingrese la distancia en km'}),  # Campo de desarrollo
            'energia': forms.NumberInput(attrs={'placeholder': 'Ingrese el consumo en kWh'}),  # Campo de desarrollo
        }


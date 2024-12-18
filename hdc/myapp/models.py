from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model): 
    name = models.CharField(max_length=200)

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


from django.contrib.auth.models import User

class Huella(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    DIETAS = [
        ('dieta_omnivora', 'Omnivora'),
        ('dieta_vegetariana', 'Vegetariana'),
        ('dieta_vegana', 'Vegana'),
    ]
    TRANSPORTE = [
        ('transporte_auto', 'Auto'),
        ('transporte_publico', 'Público'),
        ('transporte_bicicleta', 'Bicicleta'),
        ('transporte_pie', 'A pie'),
    ]
    dieta = models.CharField(max_length=50, choices = DIETAS)
    transporte = models.CharField(max_length=50, choices= TRANSPORTE)
    distancia = models.FloatField()
    energia = models.FloatField()
    co2_emisiones = models.FloatField(default=0.0)
    fecha = models.DateTimeField(default=timezone.now)

    def calcular_huella(self):
        co2 = 0
        # Transporte
        if self.transporte == 'transporte_auto':
            co2 += self.distancia * 0.21
        elif self.transporte == 'transporte_publico':
            co2 += self.distancia * 0.10
        elif self.transporte in ['transporte_bicicleta', 'transporte_pie']:
            co2 += 0  # Sin emisiones de CO₂

        co2 += self.energia * 0.5

        # Dieta
        if self.dieta == 'dieta_omnivora':
            co2 += 2.5
        elif self.dieta == 'dieta_vegetariana':
            co2 += 1.7
        elif self.dieta == 'dieta_vegana':
            co2 += 1.0

        return co2



class Location(models.Model):
    name = models.CharField(max_length=250, verbose_name="Nombre de edificio")
    address = models.CharField(max_length=250, verbose_name="Dirección")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
 

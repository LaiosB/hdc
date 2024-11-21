# Generated by Django 5.1.2 on 2024-11-16 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_huella_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='huella',
            name='distancia',
            field=models.IntegerField(help_text='Ingrese la distancia promedio en Km'),
        ),
        migrations.AlterField(
            model_name='huella',
            name='energia',
            field=models.IntegerField(help_text='Ingrese su consummo de energia mensual en KWh'),
        ),
        migrations.AlterField(
            model_name='huella',
            name='transporte',
            field=models.CharField(choices=[('transporte_auto', 'Auto'), ('transporte_publico', 'Publico'), ('transporte_bicicleta', 'Bicicleta'), ('transporte_pie', 'A pie')], max_length=30),
        ),
    ]

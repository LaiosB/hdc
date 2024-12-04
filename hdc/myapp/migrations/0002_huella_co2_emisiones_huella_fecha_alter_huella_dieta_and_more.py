# Generated by Django 5.1.3 on 2024-12-03 00:47

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='huella',
            name='co2_emisiones',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='huella',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='huella',
            name='dieta',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='huella',
            name='distancia',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='huella',
            name='energia',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='huella',
            name='transporte',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='huella',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
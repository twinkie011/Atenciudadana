# Generated by Django 5.1.7 on 2025-05-10 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apoyos', '0026_solicitud_clave_elector_solicitud_seccion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='seccion',
            field=models.CharField(blank=True, max_length=4, verbose_name='Sección Electoral'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='vigencia',
            field=models.CharField(blank=True, max_length=10, verbose_name='Vigencia de INE'),
        ),
    ]

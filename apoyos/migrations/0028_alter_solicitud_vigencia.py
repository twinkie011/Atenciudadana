# Generated by Django 5.1.7 on 2025-05-10 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apoyos', '0027_alter_solicitud_seccion_alter_solicitud_vigencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='vigencia',
            field=models.CharField(blank=True, max_length=9, verbose_name='Vigencia de INE'),
        ),
    ]

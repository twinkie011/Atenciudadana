# Generated by Django 5.1.7 on 2025-04-09 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0010_alter_municipiocp_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='municipiocp',
            options={'verbose_name': 'Municipio con CP', 'verbose_name_plural': 'Municipios con CP'},
        ),
    ]

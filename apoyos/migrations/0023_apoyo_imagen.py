# Generated by Django 5.1.7 on 2025-04-26 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apoyos', '0022_quejasugerencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='apoyo',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='apoyos/', verbose_name='Imagen del apoyo'),
        ),
    ]

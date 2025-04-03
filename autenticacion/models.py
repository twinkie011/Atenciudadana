from django.contrib.auth.models import AbstractUser
from django.db import models
from .models import Municipio  # Asegúrate de que Municipio esté en el mismo archivo o importado si está en otra app

class Municipio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    domicilio = models.CharField(max_length=255)
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True)
    codigo_postal = models.CharField(max_length=10)
    telefono = models.CharField(max_length=10)

    USERNAME_FIELD = 'email'  # Login será por correo
    REQUIRED_FIELDS = ['username', 'nombre', 'apellidos']  # Campos obligatorios además del email y password

    def __str__(self):
        return self.email

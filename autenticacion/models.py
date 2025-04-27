from django.contrib.auth.models import AbstractUser
from django.db import models

# Modelo de Municipios (para que puedan ser seleccionados al registrar usuarios)
class Municipio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    curp = models.CharField(max_length=18, unique=True, verbose_name="CURP")
    domicilio = models.CharField(max_length=255)
    municipio = models.ForeignKey('autenticacion.Municipio', on_delete=models.SET_NULL, null=True)
    codigo_postal = models.CharField(max_length=5)
    telefono = models.CharField(max_length=10)


    ROLES = [
        ('usuario', 'Usuario'),
        ('administrador', 'Administrador'),
        ('alcalde', 'Alcalde (Superadmin)'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellidos']

    def __str__(self):
        return self.email

class MunicipioCP(models.Model):
    municipio = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.municipio} ({self.codigo_postal})"


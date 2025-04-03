from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

# Función para validar que la fecha de fin no sea anterior a la de inicio
def validar_fechas(fecha_fin, fecha_inicio):
    if fecha_fin < fecha_inicio:
        raise ValidationError("La fecha de finalización no puede ser anterior a la fecha de inicio.")

class Apoyo(models.Model):
    TIPOS_APOYO = [
        ('alimentario', 'Alimentario'),
        ('económico', 'Económico'),
        ('vivienda', 'Vivienda'),
    ]

    DISPONIBILIDAD_CHOICES = [
        (True, 'Disponible'),
        (False, 'No disponible'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre del apoyo")
    descripcion_corta = models.TextField(max_length=250, default="Descripción breve")
    descripcion = models.TextField(verbose_name="Descripción completa")
    # imagen = models.ImageField(upload_to='apoyos', null=True, blank=True)
    tipo = models.CharField(max_length=50, choices=TIPOS_APOYO, verbose_name="Tipo de apoyo")
    
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de finalización")
    disponible = models.BooleanField(choices=DISPONIBILIDAD_CHOICES, default=True, verbose_name="Disponibilidad")

    

    class Meta:
        ordering = ['fecha_inicio']
        verbose_name = "Apoyo"
        verbose_name_plural = "Apoyos"

    def clean(self):
        validar_fechas(self.fecha_fin, self.fecha_inicio)

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    apoyo = models.ForeignKey(Apoyo, on_delete=models.CASCADE, verbose_name="Apoyo solicitado")
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de solicitud")

    class Meta:
        ordering = ['-fecha_solicitud']
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"

    def __str__(self):
        return f"{self.usuario.username} - {self.apoyo.nombre}"


class Requisito(models.Model):
    apoyo = models.ForeignKey(Apoyo, on_delete=models.CASCADE, related_name="requisitos", verbose_name="Apoyo")
    descripcion = models.TextField(verbose_name="Descripción del requisito")

    class Meta:
        verbose_name = "Requisito"
        verbose_name_plural = "Requisitos"

    def __str__(self):
        return f"{self.apoyo.nombre} - {self.descripcion[:50]}"
    
    motivo = models.TextField(null=True, blank=True)
    ingresos = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Pregunta(models.Model):
    texto = models.CharField(max_length=255)
    obligatoria = models.BooleanField(default=True)

    def __str__(self):
        return self.texto

class Respuesta(models.Model):
    solicitud = models.ForeignKey('Solicitud', on_delete=models.CASCADE, related_name='respuestas')
    pregunta = models.ForeignKey('Pregunta', on_delete=models.CASCADE)
    respuesta_texto = models.TextField()

    def __str__(self):
        return f"{self.pregunta.texto} - {self.respuesta_texto[:30]}"



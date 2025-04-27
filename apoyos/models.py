from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from datetime import date

# -----------------------------------------------
# MODELO: Tipo de Apoyo (usado como catálogo)
# -----------------------------------------------
class TipoApoyo(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del tipo de apoyo")

    class Meta:
        verbose_name = "Tipo de Apoyo"
        verbose_name_plural = "Tipos de Apoyo"

    def __str__(self):
        return self.nombre


# -----------------------------------------------
# MODELO: Apoyo
# -----------------------------------------------
class Apoyo(models.Model):
    DISPONIBILIDAD_CHOICES = [
        (True, 'Disponible'),
        (False, 'No disponible'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre del apoyo")
    descripcion_corta = models.TextField(max_length=400)
    descripcion = models.TextField(verbose_name="Descripción completa")

    tipo = models.ForeignKey(TipoApoyo, on_delete=models.CASCADE, verbose_name="Tipo de apoyo")  # nuevo

    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de finalización")

    disponible = models.BooleanField(choices=DISPONIBILIDAD_CHOICES, default=True, verbose_name="Disponibilidad")

    imagen = models.ImageField(upload_to='apoyos/', blank=True, null=True, verbose_name="Imagen del apoyo")  # 🟢 Campo nuevo

    publicado = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['fecha_inicio']
        verbose_name = "Apoyo"
        verbose_name_plural = "Apoyos"

    def clean(self):
        # 1. Que la fecha de fin no sea anterior a la de inicio
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha de finalización no puede ser anterior a la fecha de inicio.")

        # 2. Que la fecha de inicio no sea anterior a hoy
        if self.fecha_inicio < date.today():
            raise ValidationError("La fecha de inicio no puede estar en el pasado.")

        # 3. Que no exceda 3 meses de duración
        delta = self.fecha_fin - self.fecha_inicio
        if delta.days > 93:
            raise ValidationError("Un apoyo no puede durar más de 3 meses (93 días).")

    def __str__(self):
        return self.nombre

# -----------------------------------------------
# MODELO: Solicitud (modificado con campos nuevos)
# -----------------------------------------------
class Solicitud(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuario")
    apoyo = models.ForeignKey(Apoyo, on_delete=models.CASCADE, verbose_name="Apoyo solicitado")
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de solicitud")

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name="Estado")

    # ✅ CAMPOS NUEVOS
    situacion = models.TextField(verbose_name="Situación actual", blank=True)
    ocupacion = models.CharField(max_length=100, verbose_name="Ocupación", blank=True)
    educacion = models.CharField(max_length=50, verbose_name="Nivel educativo", blank=True)
    vivienda = models.CharField(max_length=50, verbose_name="Tipo de vivienda", blank=True)
    mayor_edad = models.BooleanField(default=False)
    condiciones = models.BooleanField(default=False)

    motivo_rechazo = models.TextField(blank=True, null=True, verbose_name="Motivo de rechazo")
    
    class Meta:
        ordering = ['-fecha_solicitud']
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"

    def __str__(self):
        return f"{self.usuario.email} - {self.apoyo.nombre} ({self.estado})"


# -----------------------------------------------
# MODELO: Requisito (para cada apoyo)
# -----------------------------------------------
class Requisito(models.Model):
    apoyo = models.ForeignKey(Apoyo, on_delete=models.CASCADE, related_name="requisitos", verbose_name="Apoyo")
    descripcion = models.TextField(verbose_name="Descripción del requisito")

    # Campos socioeconómicos opcionales
    motivo = models.TextField(null=True, blank=True)
    ingresos = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Requisito"
        verbose_name_plural = "Requisitos"

    def __str__(self):
        return f"{self.apoyo.nombre} - {self.descripcion[:50]}"


# -----------------------------------------------
# MODELO: Pregunta de cuestionario
# -----------------------------------------------
class Pregunta(models.Model):
    texto = models.CharField(max_length=255)
    obligatoria = models.BooleanField(default=True)

    def __str__(self):
        return self.texto


# -----------------------------------------------
# MODELO: Respuesta de cuestionario
# -----------------------------------------------
class Respuesta(models.Model):
    solicitud = models.ForeignKey('Solicitud', on_delete=models.CASCADE, related_name='respuestas')
    pregunta = models.ForeignKey('Pregunta', on_delete=models.CASCADE)
    respuesta_texto = models.TextField()

    def __str__(self):
        return f"{self.pregunta.texto} - {self.respuesta_texto[:30]}"
    
class DocumentoRequisito(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='documentos')
    requisito = models.ForeignKey(Requisito, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='documentos_requisitos/', validators=[
        FileExtensionValidator(['pdf'])
    ])
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.solicitud.usuario} - {self.requisito.descripcion[:30]}"



from django.db import models
from autenticacion.models import CustomUser

class QuejaSugerencia(models.Model):
    TIPOS = [
        ('queja', 'Queja'),
        ('sugerencia', 'Sugerencia'),
    ]

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('leida', 'Leída'),
        ('archivada', 'Archivada'),
    ]

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"{self.tipo.title()} de {self.usuario.nombre}"

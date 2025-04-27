from django.db import models
from django.conf import settings

class Sugerencia(models.Model):
    TIPO_CHOICES = [
        ('queja', 'Queja'),
        ('sugerencia', 'Sugerencia'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.usuario.get_full_name()}"

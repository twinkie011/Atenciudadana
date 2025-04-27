from django.db import models
from django.utils import timezone

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    imagen = models.ImageField(upload_to='noticias/', blank=True, null=True)

    def __str__(self):
        return self.titulo

from django.urls import path
from .views import enviar_sugerencia

urlpatterns = [
    path('enviar/', enviar_sugerencia, name='enviar_sugerencia'),
]

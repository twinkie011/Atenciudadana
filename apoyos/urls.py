from django.urls import path
from .views import inicio, detalle_apoyo, solicitar_apoyo

urlpatterns = [
    path('', inicio, name='inicio'),
    path('solicitar_apoyo/<int:apoyo_id>/', solicitar_apoyo,
     name='solicitar_apoyo'),
     
     path('detalle_apoyo/<int:apoyo_id>/', detalle_apoyo,
          name='detalle_apoyo'),
]


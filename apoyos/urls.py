from django.urls import path
from .views import (
    inicio, detalle_apoyo, solicitar_apoyo,
    listar_tipos_apoyo, crear_tipo_apoyo,
    editar_tipo_apoyo, eliminar_tipo_apoyo,reemplazar_documento,todos_los_apoyos
)

urlpatterns = [
    # Vistas públicas
    path('', inicio, name='inicio'),
    path('detalle_apoyo/<int:apoyo_id>/', detalle_apoyo, name='detalle_apoyo'),
    path('solicitar_apoyo/<int:apoyo_id>/', solicitar_apoyo, name='solicitar_apoyo'),

    # Módulo Tipos de Apoyo (para alcalde y administrador)
    path('tipos/', listar_tipos_apoyo, name='listar_tipos_apoyo'),
    path('tipos/crear/', crear_tipo_apoyo, name='crear_tipo_apoyo'),
    path('tipos/editar/<int:tipo_id>/', editar_tipo_apoyo, name='editar_tipo_apoyo'),
    path('tipos/eliminar/<int:tipo_id>/', eliminar_tipo_apoyo, name='eliminar_tipo_apoyo'),
    path('documento/reemplazar/<int:id>/', reemplazar_documento, name='reemplazar_documento'),
    path('apoyos_usurarios/', todos_los_apoyos, name='lista_apoyo'),
]

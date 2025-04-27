from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.panel_administrador, name='panel_administrador'),
    
    path('apoyos/', views.listar_apoyos, name='listar_apoyos_admin'),
    path('apoyos/crear/', views.crear_apoyo, name='crear_apoyo_admin'),
    path('apoyos/editar/<int:apoyo_id>/', views.editar_apoyo, name='editar_apoyo_admin'),
    path('apoyos/eliminar/<int:apoyo_id>/', views.eliminar_apoyo, name='eliminar_apoyo_admin'),

    path('solicitudes/', views.listar_solicitudes_view, name='listar_solicitudes_admin'),
    path('solicitudes/<int:solicitud_id>/', views.detalle_solicitud_view, name='detalle_solicitud_admin'),

    path('solicitudes/', views.listar_solicitudes_admin, name='listar_solicitudes_admin'),
    path('solicitudes/<int:solicitud_id>/', views.detalle_solicitud_admin, name='detalle_solicitud_admin'),
    path('solicitudes/<int:solicitud_id>/editar/', views.editar_solicitud_admin, name='editar_solicitud_admin'),
]

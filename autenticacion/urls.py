from django.urls import path
from .views import (
    registro_view, LoginUsuarioView, panel_usuario,
    obtener_municipio_por_cp, obtener_cp_por_municipio,mis_solicitudes_view,detalle_solicitud_usuario_view,editar_perfil
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('registro/', registro_view, name='registro'),
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('panel/', panel_usuario, name='panel_usuario'),

    # AJAX endpoints
    path('ajax/municipio-por-cp/', obtener_municipio_por_cp, name='municipio_por_cp'),
    path('ajax/cp-por-municipio/', obtener_cp_por_municipio, name='cp_por_municipio'),

    path('mis-solicitudes/', mis_solicitudes_view, name='mis_solicitudes'),
    path('solicitud/<int:solicitud_id>/', detalle_solicitud_usuario_view, name='detalle_solicitud_usuario'),
    path('editar-perfil/', editar_perfil, name='editar_perfil'),
    


]

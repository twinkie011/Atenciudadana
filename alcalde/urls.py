from django.urls import path
from .views import panel_alcalde, crear_administrador_view,listado_administradores_view,editar_administrador_view,eliminar_administrador_view,listar_solicitudes_view,detalle_solicitud_alcalde,editar_solicitud_alcalde,apoyos_mas_solicitados,generar_pdf_apoyo,generar_pdf_apoyos_totales,listar_sugerencias_view
from apoyos import views as banner_views
from . import views 

urlpatterns = [
    path('panel/', panel_alcalde, name='panel_alcalde'),
    path('crear-admin/', crear_administrador_view, name='crear_administrador'),
    path('administradores/', listado_administradores_view, name='listado_administradores'),
    path('editar-admin/<int:admin_id>/', editar_administrador_view, name='editar_administrador'),
    path('eliminar-admin/<int:admin_id>/', eliminar_administrador_view, name='eliminar_administrador'),


    path('apoyos/', views.listar_apoyos, name='listar_apoyos'),
    path('apoyos/crear/', views.crear_apoyo, name='crear_apoyo'),
    path('apoyos/editar/<int:apoyo_id>/', views.editar_apoyo, name='editar_apoyo'),
    path('apoyos/eliminar/<int:apoyo_id>/', views.eliminar_apoyo, name='eliminar_apoyo'),

    path('solicitudes/', listar_solicitudes_view, name='solicitudes_alcalde'),
    path('solicitudes/<int:solicitud_id>/', detalle_solicitud_alcalde, name='detalle_solicitud_alcalde'),
    path('solicitud/<int:solicitud_id>/editar/', editar_solicitud_alcalde, name='editar_solicitud_alcalde'),
    path('estadisticas/apoyos-mas-solicitados/', apoyos_mas_solicitados, name='apoyos_mas_solicitados'),
    path('apoyo/<int:apoyo_id>/pdf/', generar_pdf_apoyo, name='generar_pdf_apoyo'),
    path('estadisticas/pdf-apoyos/', generar_pdf_apoyos_totales, name='generar_pdf_apoyos_totales'),
    path('sugerencias/', listar_sugerencias_view, name='listar_sugerencias'),
    
    
    path('banners/', banner_views.lista_banners, name='lista_banners'),
    path('banners/crear/', banner_views.crear_banner, name='crear_banner'),
    path('banners/eliminar/<int:banner_id>/', banner_views.eliminar_banner, name='eliminar_banner'),
    


    path('exportar-solicitudes-excel/', views.exportar_excel_solicitudes, name='exportar_excel_solicitudes'),




]

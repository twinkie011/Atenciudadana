from django.urls import path
from . import views

urlpatterns = [
    # Compartidas entre alcalde y administrador
    path('noticias/', views.listar_noticias, name='listar_noticias'),
    path('noticias/crear/', views.crear_noticia, name='crear_noticia'),
    path('noticias/editar/<int:noticia_id>/', views.editar_noticia, name='editar_noticia'),
    path('noticias/eliminar/<int:noticia_id>/', views.eliminar_noticia, name='eliminar_noticia'),

    # Vista pública para usuarios normales
    path('noticias/usuario/', views.listar_noticias_usuario, name='listar_noticias_usuario'),
    path('noticias/usuario/<int:noticia_id>/', views.detalle_noticia_usuario, name='detalle_noticia_usuario'),
     path('noticia/<int:noticia_id>/', views.detalle_noticia_usuario, name='detalle_noticia_usuario'),
]

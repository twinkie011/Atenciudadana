from django.contrib import admin
from django.urls import path, include
from apoyos.views import inicio, solicitar_apoyo, detalle_apoyo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name='inicio'),
    path('', include('autenticacion.urls')),
    path('cuentas/', include('autenticacion.urls')),
    path('solicitar_apoyo/<int:apoyo_id>/', solicitar_apoyo, name='solicitar_apoyo'),
    path('detalle_apoyo/<int:apoyo_id>/', detalle_apoyo, name='detalle_apoyo'),
    path('alcalde/', include('alcalde.urls')),
    path('apoyos/', include('apoyos.urls')),
    path('sugerencias/', include('sugerencias.urls')),
    path('noticias/', include('noticias.urls')),
    path('admin-dashboard/', include('administrador.urls')),

]

# 🟢 Habilitar archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from apoyos.views import inicio, solicitar_apoyo, detalle_apoyo
from autenticacion.views import CustomPasswordResetView
from django.contrib.auth import views as auth_views
from autenticacion.views import CustomPasswordResetConfirmView
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

    # ✅ Recuperar contraseña
    path('recuperar/', CustomPasswordResetView.as_view(
        template_name='recuperacion/recuperar_contrasena.html',
        html_email_template_name='recuperacion/email_contrasena.html',
    ), name='password_reset'),

    # 2. Confirmación de que se envió el correo
    path('recuperar/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='recuperacion/recuperar_contrasena.html'
    ), name='password_reset_done'),

    # 3. Cambiar contraseña (desde link con token)
    path('recuperar/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # 4. Contraseña restablecida correctamente
    path('recuperar/completo/', auth_views.PasswordResetCompleteView.as_view(
        template_name='recuperacion/recuperar_contrasena.html'
    ), name='password_reset_complete'),
]

# 🟢 Habilitar archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

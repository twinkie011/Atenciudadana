from django.contrib import admin
from .models import Apoyo, Solicitud, Requisito, Pregunta, Respuesta

# Configurar inline para agregar requisitos dentro de la vista de Apoyo
class RequisitoInline(admin.TabularInline):  
    model = Requisito
    extra = 1  # Muestra un formulario vacío para agregar requisitos nuevos

# Configurar la administración de Apoyo
class ApoyoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'fecha_inicio', 'fecha_fin', 'disponible')
    search_fields = ('nombre', 'tipo')
    list_filter = ('tipo', 'disponible')
    inlines = [RequisitoInline]  # Agregar requisitos dentro de Apoyo

# Configurar la administración de Solicitudes
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'apoyo', 'fecha_solicitud')
    search_fields = ('usuario__username', 'apoyo__nombre')

# Registrar modelos en el panel de administración
admin.site.register(Apoyo, ApoyoAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Requisito)  # Registrar requisitos en el admin
admin.site.register(Pregunta)
admin.site.register(Respuesta)

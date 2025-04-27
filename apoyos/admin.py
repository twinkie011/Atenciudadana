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
 

# Registrar modelos en el panel de administración
admin.site.register(Apoyo, ApoyoAdmin)

admin.site.register(Requisito)  # Registrar requisitos en el admin
admin.site.register(Pregunta)
admin.site.register(Respuesta)

from django.contrib import admin
from .models import Solicitud, Apoyo, Requisito, DocumentoRequisito, Pregunta, Respuesta





from django.contrib import admin
from .models import Solicitud, Apoyo, Requisito, DocumentoRequisito, Pregunta, Respuesta

# Inline para Documentos
class DocumentoRequisitoInline(admin.TabularInline):
    model = DocumentoRequisito
    extra = 0
    fields = ('requisito', 'archivo', 'estado', 'observaciones')
    readonly_fields = ('archivo',)
    can_delete = False

# Inline para Respuestas
class RespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 0
    fields = ('pregunta', 'respuesta_texto')
    readonly_fields = ('pregunta', 'respuesta_texto')
    can_delete = False

# Solicitud Admin con inlines
@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'apoyo', 'estado', 'fecha_solicitud')
    list_filter = ('estado', 'apoyo')
    search_fields = ('usuario__email', 'usuario__nombre', 'usuario__apellidos', 'apoyo__nombre')
    readonly_fields = ('fecha_solicitud',)

    inlines = [DocumentoRequisitoInline, RespuestaInline]

    fieldsets = (
        ("Datos generales", {
            'fields': ('usuario', 'apoyo', 'estado')
        }),
        ("Información extendida del solicitante", {
            'fields': ('situacion', 'ocupacion', 'educacion', 'vivienda', 'mayor_edad', 'condiciones')
        }),
        ("Seguimiento", {
            'fields': ('motivo_rechazo', 'fecha_solicitud')
        }),
    )

    actions = ['aprobar_solicitud', 'rechazar_solicitud']

    # Acción personalizada para aprobar
    def aprobar_solicitud(self, request, queryset):
        updated = queryset.update(estado='aprobada')
        self.message_user(request, f"{updated} solicitud(es) aprobada(s) exitosamente.")
    aprobar_solicitud.short_description = "Aprobar solicitudes seleccionadas"

    # Acción personalizada para rechazar
    def rechazar_solicitud(self, request, queryset):
        updated = queryset.update(estado='rechazada')
        self.message_user(request, f"{updated} solicitud(es) rechazada(s) exitosamente.")
    rechazar_solicitud.short_description = "Rechazar solicitudes seleccionadas"


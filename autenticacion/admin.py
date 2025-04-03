from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Municipio

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'nombre', 'apellidos', 'municipio', 'telefono', 'is_staff')
    search_fields = ('email', 'nombre', 'apellidos')
    ordering = ('email',)

    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('nombre', 'apellidos', 'domicilio', 'municipio', 'codigo_postal', 'telefono')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Municipio)

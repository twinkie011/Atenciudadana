from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Municipio, MunicipioCP
from django import forms

class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_curp(self):
        curp = self.cleaned_data['curp'].upper()
        if not curp.isalnum():
            raise forms.ValidationError("La CURP solo debe contener letras y números.")
        return curp

    def clean_codigo_postal(self):
        cp = self.cleaned_data['codigo_postal']
        if not cp.isdigit():
            raise forms.ValidationError("El código postal solo debe contener números.")
        return cp

    def clean_telefono(self):
        tel = self.cleaned_data['telefono']
        if not tel.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números.")
        return tel

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserAdminForm
    form = CustomUserAdminForm
    model = CustomUser
    list_display = ('email', 'nombre', 'apellidos', 'rol', 'municipio')
    list_filter = ('rol', 'municipio')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'apellidos', 'curp', 'domicilio', 'municipio', 'codigo_postal', 'telefono')}),
        ('Permisos', {'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'nombre', 'apellidos', 'curp', 'domicilio', 'municipio', 'codigo_postal', 'telefono', 'rol', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('email', 'nombre', 'curp')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

# También registra Municipios por si necesitas gestionarlos
@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    ordering = ('nombre',)

@admin.register(MunicipioCP)
class MunicipioCPAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'codigo_postal')
    search_fields = ('municipio', 'codigo_postal')

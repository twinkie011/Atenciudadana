from django import forms
from .models import Apoyo, TipoApoyo, Solicitud
import re


class CuestionarioSolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'situacion',
            'ocupacion',
            'educacion',
            'vivienda',
            'condiciones',
            'mayor_edad',
            'clave_elector',
            'seccion',
            'vigencia',
        ]
        labels = {
            'situacion': 'Describe tu situación actual',
            'ocupacion': 'Ocupación',
            'educacion': 'Nivel Educativo',
            'vivienda': 'Tipo de Vivienda',
            'condiciones': 'He leído y acepto los requisitos del apoyo',
            'mayor_edad': 'Declaro que soy mayor de 18 años',
            'clave_elector': 'Clave de Elector',
            'seccion': 'Sección Electoral',
            'vigencia': 'Vigencia de la INE (formato: 2026-2036)',
        }
        widgets = {
            'situacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control'}),
            'educacion': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('primaria', 'Primaria'),
                ('secundaria', 'Secundaria'),
                ('bachillerato', 'Bachillerato'),
                ('universidad', 'Universidad'),
            ]),
            'vivienda': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('propia', 'Propia'),
                ('rentada', 'Rentada'),
                ('prestada', 'Prestada'),
            ]),
            'condiciones': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'mayor_edad': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'clave_elector': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 18,
                'placeholder': 'Ej. ABCD123456EFGHI789'
            }),
            'seccion': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 4,
                'placeholder': 'Ej. 0456'
            }),
            'vigencia': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 9,
                'placeholder': 'Ej. 2026-2036'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        clave = cleaned_data.get("clave_elector")
        seccion = cleaned_data.get("seccion")
        vigencia = cleaned_data.get("vigencia")
        anio_actual = date.today().year

        if clave and not re.fullmatch(r'[A-Z0-9]{18}', clave):
            self.add_error('clave_elector', "La clave debe tener exactamente 18 caracteres, solo letras mayúsculas y números.")

        if seccion and not re.fullmatch(r'\d{4}', seccion):
            self.add_error('seccion', "La sección debe contener exactamente 4 dígitos.")

        if vigencia:
            if not re.fullmatch(r'\d{4}-\d{4}', vigencia):
                self.add_error('vigencia', "El formato debe ser AAAA-AAAA (ej. 2026-2036).")
            else:
                a1, a2 = map(int, vigencia.split('-'))
                if a1 < anio_actual:
                    self.add_error('vigencia', f"El primer año debe ser igual o mayor a {anio_actual}.")
                elif a2 <= a1:
                    self.add_error('vigencia', "El segundo año debe ser mayor al primero.")

from datetime import date
from django import forms
from .models import Apoyo

class ApoyoForm(forms.ModelForm):
    class Meta:
        model = Apoyo
        fields = [
            'nombre',
            'descripcion_corta',
            'descripcion',
            'tipo',
            'fecha_inicio',
            'fecha_fin',
            'disponible',
            'imagen',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_corta': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'disponible': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.editar = kwargs.pop('editar', False)  # 👈 importante
        super().__init__(*args, **kwargs)

        for field in ['fecha_inicio', 'fecha_fin']:
            if self.instance and getattr(self.instance, field):
                self.fields[field].initial = getattr(self.instance, field).strftime('%Y-%m-%d')

        if self.editar:
            # ❗️Importante: marcar como deshabilitado visualmente
           self.fields['fecha_inicio'].disabled = True 

    def clean_fecha_inicio(self):
        if self.editar:
            return self.instance.fecha_inicio
        return self.cleaned_data.get('fecha_inicio')



class TipoApoyoForm(forms.ModelForm):
    class Meta:
        model = TipoApoyo
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Económico, Alimentario...'
            }),
        }

        
from django import forms
from .models import Banner

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['titulo', 'imagen', 'orden']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import Apoyo, TipoApoyo, Solicitud

class CuestionarioSolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'situacion', 'ocupacion', 'educacion',
            'vivienda', 'condiciones', 'mayor_edad'
        ]
        labels = {
            'situacion': 'Describe tu situación actual',
            'ocupacion': 'Ocupación',
            'educacion': 'Nivel Educativo',
            'vivienda': 'Tipo de Vivienda',
            'condiciones': 'He leído y acepto los requisitos del apoyo',
            'mayor_edad': 'Declaro que soy mayor de 18 años',
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
        }


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
        super().__init__(*args, **kwargs)
        for field in ['fecha_inicio', 'fecha_fin']:
            if self.instance and getattr(self.instance, field):
                self.fields[field].initial = getattr(self.instance, field).strftime('%Y-%m-%d')


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

        

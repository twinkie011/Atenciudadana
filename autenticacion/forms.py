from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Municipio
from django.core.validators import RegexValidator

solo_numeros = RegexValidator(r'^\d+$', 'Este campo solo permite números.')
solo_letras = RegexValidator(r'^[A-Za-zÁÉÍÓÚÑáéíóúñ\s]+$', 'Este campo solo permite letras.')
curp_valido = RegexValidator(r'^[A-Z0-9]+$', 'La CURP solo debe contener letras mayúsculas y números.')

class RegistroForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['curp', 'nombre', 'apellidos', 'domicilio', 'codigo_postal', 'municipio',
                  'email', 'telefono', 'password1', 'password2']

        widgets = {
            'curp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'TEMP000000XXXXXX00(s)',
                'maxlength': '18'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre(s)',
                'pattern': '[A-Za-zÁÉÍÓÚÑáéíóúñ\\s]+',
                'title': 'Solo letras'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos',
                'pattern': '[A-Za-zÁÉÍÓÚÑáéíóúñ\\s]+',
                'title': 'Solo letras'
            }),
            'domicilio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Calle y número'
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código Postal',
                'pattern': '\\d+',
                'title': 'Solo números'
             }),
            'municipio': forms.Select(attrs={
                'class': 'form-select'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 9991234567',
                'pattern': '\\d+',
                'title': 'Solo números'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['municipio'].queryset = Municipio.objects.all().order_by('nombre')
        self.fields['codigo_postal'].validators.append(solo_numeros)
        self.fields['telefono'].validators.append(solo_numeros)
        self.fields['curp'].validators.append(curp_valido)
        self.fields['nombre'].validators.append(solo_letras)
        self.fields['apellidos'].validators.append(solo_letras)

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_curp(self):
        curp = self.cleaned_data.get('curp')
        if CustomUser.objects.filter(curp=curp).exists():
            raise forms.ValidationError("Esta CURP ya está registrada.")
        return curp


# autenticacion/forms.py

from django import forms
from .models import CustomUser  # Asegúrate que es tu modelo de usuario

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nombre', 'apellidos', 'telefono', 'domicilio', 'municipio', 'codigo_postal']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'domicilio': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.Select(attrs={'class': 'form-select'}),  # si es ForeignKey
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
        }

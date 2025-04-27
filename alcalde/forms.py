from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from autenticacion.models import CustomUser, Municipio

# Validadores
solo_numeros = RegexValidator(r'^\d+$', 'Este campo solo permite números.')
solo_letras = RegexValidator(r'^[A-Za-zÁÉÍÓÚÑáéíóúñ\s]+$', 'Este campo solo permite letras.')
curp_valido = RegexValidator(r'^[A-Z0-9]+$', 'La CURP solo debe contener letras mayúsculas y números.')

class CrearAdministradorForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['nombre', 'apellidos', 'email', 'telefono', 'domicilio', 'municipio', 'codigo_postal', 'curp', 'password1', 'password2']

        widgets = {
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
            'curp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'TEMP000000XXXXXX00(s)',
                'maxlength': '18'
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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 'administrador'
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = CustomUser.objects.filter(email=email)

        # Si estamos editando, excluimos el mismo usuario
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_curp(self):
        curp = self.cleaned_data.get('curp')
        qs = CustomUser.objects.filter(curp=curp)

        # Si estamos editando, excluimos el mismo usuario
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Esta CURP ya está registrada.")
        return curp


class EditarAdministradorForm(CrearAdministradorForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Desactivar los campos curp y email
        self.fields['curp'].disabled = True
        self.fields['email'].disabled = True

        # Hacer opcionales las contraseñas para edición
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def clean_email(self):
        # Si el campo está desactivado, no hagas validación
        return self.instance.email

    def clean_curp(self):
        return self.instance.curp

    def clean_password2(self):
        # Si se ingresó password, validamos normalmente
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)

        # Si se proporcionó una nueva contraseña, se actualiza
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)

        if commit:
            user.save()
        return user

from django import forms
from apoyos.models import DocumentoRequisito

class RevisarDocumentoForm(forms.ModelForm):
    class Meta:
        model = DocumentoRequisito
        fields = ['estado', 'observaciones']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}, choices=DocumentoRequisito.ESTADOS),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Opcional: comentarios sobre este documento...'
            }),
        }

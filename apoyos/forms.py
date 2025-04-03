from django import forms

class CuestionarioSolicitudForm(forms.Form):
    motivo = forms.CharField(
        label='¿Por qué solicitas este apoyo?',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    ingresos = forms.DecimalField(
        label='¿Cuál es tu ingreso mensual aproximado?',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    condiciones = forms.BooleanField(
        label='Confirmo que he leído y cumplo con los requisitos del apoyo',
        required=True
    )

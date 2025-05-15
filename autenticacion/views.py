from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import RegistroForm
from .models import MunicipioCP
from apoyos.models import Solicitud
from django.contrib.auth import authenticate, login


class LoginUsuarioView(LoginView):
    template_name = 'autenticacion/login.html'
    authentication_form = AuthenticationForm


@login_required
def panel_usuario(request):
    solicitudes = Solicitud.objects.filter(usuario=request.user).select_related('apoyo')
    return render(request, 'usuarios/panel_usuario.html', {'solicitudes': solicitudes})


def obtener_municipio_por_cp(request):
    cp = request.GET.get('codigo_postal')
    if cp:
        resultado = MunicipioCP.objects.filter(codigo_postal=cp).first()
        if resultado:
            return JsonResponse({'municipio': resultado.municipio})
    return JsonResponse({'municipio': None})


def obtener_cp_por_municipio(request):
    municipio = request.GET.get('municipio')
    if municipio:
        resultado = MunicipioCP.objects.filter(municipio=municipio).first()
        if resultado:
            return JsonResponse({'codigo_postal': resultado.codigo_postal})
    return JsonResponse({'codigo_postal': None})


from django.contrib.auth import logout

def logout_manual(request):
    logout(request)
    return redirect('login')


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()

            # Autenticar e iniciar sesión automáticamente
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=usuario.email, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirigir al inicio

    else:
        form = RegistroForm()

    return render(request, 'autenticacion/registro.html', {'form': form})

@login_required
def mis_solicitudes_view(request):
    solicitudes = Solicitud.objects.filter(usuario=request.user).select_related('apoyo')
    return render(request, 'usuario/solicitudes.html', {
        'solicitudes': solicitudes
    })


from django.shortcuts import render, get_object_or_404
from apoyos.models import Solicitud
from django.contrib.auth.decorators import login_required

@login_required
def detalle_solicitud_usuario_view(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id, usuario=request.user)
    respuestas = solicitud.respuestas.select_related('pregunta').all()
    documentos = solicitud.documentos.select_related('requisito').all()

    return render(request, 'autenticacion/solicitud_detalle_usuario.html', {
        'solicitud': solicitud,
        'respuestas': respuestas,
        'documentos': documentos,
    })

# autenticacion/views.py
from django.shortcuts import render, get_object_or_404
from apoyos.models import Solicitud

def detalle_solicitud_usuario_view(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id, usuario=request.user)
    return render(request, 'autenticacion/detalle_solicitud.html', {
        'solicitud': solicitud,
    })


# autenticacion/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EditarPerfilForm

def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('panel_usuario')  # URL a tu panel de perfil
    else:
        form = EditarPerfilForm(instance=request.user)
    return render(request, 'usuarios/editar_perfil.html', {'form': form})


from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.contrib.auth import get_user_model

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data['email']
        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, 'Este correo no está registrado en el sistema.')
            return self.form_invalid(form)
        return super().form_valid(form)
    

from django.contrib.auth.views import PasswordResetConfirmView

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'recuperacion/cambiar_contrasena.html'


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Apoyo, Solicitud

# Vista de inicio que muestra los apoyos disponibles
def inicio(request):
    apoyos = Apoyo.objects.all()
    return render(request, 'apoyos/lista.html', {'apoyos': apoyos})

def detalle_apoyo(request, apoyo_id):
    apoyo = get_object_or_404(Apoyo, id=apoyo_id)
    return render(request, "apoyos/detalle.html", {"apoyo": apoyo})

# Vista para solicitar un apoyo, asegurando que no haya solicitudes duplicadas
@login_required
def solicitar_apoyo(request, apoyo_id):
    apoyo = get_object_or_404(Apoyo, id=apoyo_id)

    if Solicitud.objects.filter(usuario=request.user, apoyo=apoyo).exists():
        return render(request, 'apoyos/solicitud_existente.html', {'apoyo': apoyo})

    Solicitud.objects.create(usuario=request.user, apoyo=apoyo)
    return render(request, 'apoyos/solicitud_confirmada.html', {'apoyo': apoyo})


# Importa el formulario con las preguntas del cuestionario
from .forms import CuestionarioSolicitudForm

# Vista para solicitar un apoyo usando un formulario de cuestionario
@login_required  # Requiere que el usuario esté autenticado para acceder
def solicitar_apoyo(request, apoyo_id):
    apoyo = get_object_or_404(Apoyo, id=apoyo_id)  # Obtiene el apoyo solicitado o lanza 404

    # Verifica si el usuario ya envió una solicitud para este apoyo
    if Solicitud.objects.filter(usuario=request.user, apoyo=apoyo).exists():
        return render(request, 'apoyos/solicitud_existente.html', {'apoyo': apoyo})  # Evita solicitudes duplicadas

    if request.method == 'POST':  # Si el formulario fue enviado
        form = CuestionarioSolicitudForm(request.POST)  # Carga los datos del formulario
        if form.is_valid():  # Verifica que el formulario esté bien llenado
            Solicitud.objects.create(
                usuario=request.user,
                apoyo=apoyo
                # Puedes agregar aquí más campos si los tienes en el modelo y formulario
            )
            return render(request, 'apoyos/solicitud_confirmada.html', {'apoyo': apoyo})  # Muestra confirmación
    else:
        form = CuestionarioSolicitudForm()  # Si es GET, se muestra un formulario vacío

    return render(request, 'apoyos/formulario_solicitud.html', {'form': form, 'apoyo': apoyo})  # Renderiza el formulario

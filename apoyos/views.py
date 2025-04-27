from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Apoyo, Solicitud, TipoApoyo, Requisito, DocumentoRequisito
from .forms import CuestionarioSolicitudForm, TipoApoyoForm


# -----------------------------------------------
# VISTA DE INICIO (pública): panel_usaurio todos los apoyos
# -----------------------------------------------
def inicio(request):
    apoyos = Apoyo.objects.order_by('-fecha_inicio')[:3]
    noticias = Noticia.objects.order_by('-fecha_publicacion')[:3]
    return render(request, 'panel_usaurio.html', {'apoyos': apoyos, 'noticias': noticias})


from django.shortcuts import render
from .models import Apoyo  # Asegúrate de que tengas el modelo importado

def todos_los_apoyos(request):
    apoyos = Apoyo.objects.filter(disponible=True) 
    return render(request, 'vista/listar_apoyos.html', {'apoyos': apoyos})



# -----------------------------------------------
# DETALLE DE UN APOYO (pública)
# -----------------------------------------------
def detalle_apoyo(request, apoyo_id):
    apoyo = get_object_or_404(Apoyo, id=apoyo_id)
    return render(request, "detalles/detalle.html", {"apoyo": apoyo})


# -----------------------------------------------
# SOLICITAR APOYO (solo usuarios logueados)
# Incluye cuestionario y requisitos con PDF
# -----------------------------------------------
@login_required
def solicitar_apoyo(request, apoyo_id):
    apoyo = get_object_or_404(Apoyo, id=apoyo_id)
    requisitos = apoyo.requisitos.all()

    # Buscar solicitud existente (excepto si fue rechazada)
    solicitud_existente = Solicitud.objects.filter(
        usuario=request.user,
        apoyo=apoyo
    ).exclude(estado='rechazada').first()

    if solicitud_existente:
        if solicitud_existente.estado == 'aprobada':
            # Mostrar un mensaje especial si ya fue aprobado
            return render(request, 'detalles/solicitud_aprobada.html', {'apoyo': apoyo})
        else:
            # Si está pendiente, mensaje normal
            return render(request, 'detalles/solicitud_existente.html', {'apoyo': apoyo})

    # Si no hay solicitud previa válida, permite solicitar
    if request.method == 'POST':
        form = CuestionarioSolicitudForm(request.POST)
        archivos = request.FILES

        if form.is_valid():
            solicitud = Solicitud.objects.create(
                usuario=request.user,
                apoyo=apoyo,
                situacion=request.POST.get('situacion', ''),
                ocupacion=request.POST.get('ocupacion', ''),
                educacion=request.POST.get('educacion', ''),
                vivienda=request.POST.get('vivienda', ''),
                mayor_edad=request.POST.get('mayor_edad') == 'on',
                condiciones=request.POST.get('condiciones') == 'on',
            )

            for req in requisitos:
                archivo = archivos.get(f'requisito_{req.id}')
                if archivo:
                    DocumentoRequisito.objects.create(
                        solicitud=solicitud,
                        requisito=req,
                        archivo=archivo
                    )

            messages.success(request, "Tu solicitud ha sido enviada correctamente.")
            return render(request, 'detalles/detalle.html', {'apoyo': apoyo})

    else:
        form = CuestionarioSolicitudForm()

    return render(request, 'detalles/formulario_solicitud.html', {
        'form': form,
        'apoyo': apoyo,
        'requisitos': requisitos
    })

# -----------------------------------------------
# VISTAS PARA GESTIÓN DE TIPOS DE APOYO
# Accesibles solo por administradores y alcalde
# -----------------------------------------------

def administrador_o_alcalde(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.rol not in ['administrador', 'alcalde']:
            return HttpResponseForbidden("No tienes permiso para acceder a esta sección.")
        return view_func(request, *args, **kwargs)
    return wrapper


@administrador_o_alcalde
def listar_tipos_apoyo(request):
    tipos = TipoApoyo.objects.all().order_by('nombre')
    paginator = Paginator(tipos, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'apoyos/listar_tipos.html', {
        'tipos': page_obj,
        'page_obj': page_obj
    })


@administrador_o_alcalde
def crear_tipo_apoyo(request):
    if request.method == 'POST':
        form = TipoApoyoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de apoyo creado correctamente.")
            return redirect('listar_tipos_apoyo')
    else:
        form = TipoApoyoForm()

    return render(request, 'apoyos/crear_tipo.html', {'form': form})


@administrador_o_alcalde
def editar_tipo_apoyo(request, tipo_id):
    tipo = get_object_or_404(TipoApoyo, id=tipo_id)
    if request.method == 'POST':
        form = TipoApoyoForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de apoyo actualizado.")
            return redirect('listar_tipos_apoyo')
    else:
        form = TipoApoyoForm(instance=tipo)

    return render(request, 'apoyos/editar_tipo.html', {
        'form': form,
        'tipo': tipo
    })


@administrador_o_alcalde
def eliminar_tipo_apoyo(request, tipo_id):
    tipo = get_object_or_404(TipoApoyo, id=tipo_id)
    tipo.delete()
    messages.success(request, "Tipo de apoyo eliminado correctamente.")
    return redirect('listar_tipos_apoyo')


# (opcional: si estás usando una vista distinta para JS de nombres existentes)
def crear_tipo_apoyo_view(request):
    tipos_existentes = list(TipoApoyo.objects.values_list('nombre', flat=True))
    form = TipoApoyoForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Tipo de apoyo creado correctamente.")
        return redirect('listar_tipos_apoyo')

    return render(request, 'apoyos/crear_tipo_apoyo.html', {
        'form': form,
        'tipos_existentes': tipos_existentes
    })

# apoyos/views.py (o donde esté tu lógica de solicitudes)
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import DocumentoRequisito


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import DocumentoRequisito

@login_required
def reemplazar_documento(request, id):
    documento = get_object_or_404(DocumentoRequisito, id=id, solicitud__usuario=request.user)

    if request.method == 'POST' and request.FILES.get('archivo'):
        nuevo_archivo = request.FILES['archivo']
        documento.archivo = nuevo_archivo
        documento.estado = 'pendiente'
        documento.observaciones = ''
        documento.save()
        return redirect('detalle_solicitud_usuario', solicitud_id=documento.solicitud.id)

    return redirect('panel_usuario')


from apoyos.models import Apoyo
from noticias.models import Noticia  # 👈 Asegúrate de importar Noticia
from django.shortcuts import render

def inicio(request):
    apoyos = Apoyo.objects.order_by('-fecha_inicio')[:6]
    noticias = Noticia.objects.order_by('-fecha_publicacion')[:6]  # Carga 6 noticias más recientes
    return render(request, 'panel_usaurio.html', {'apoyos': apoyos, 'noticias': noticias})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def solo_administrador(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.rol == 'administrador':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

@login_required
@solo_administrador
def panel_administrador(request):
    return render(request, 'administrador/panel_administrador.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from apoyos.models import Apoyo, Requisito, Solicitud, DocumentoRequisito
from apoyos.forms import ApoyoForm

# ===============================================
# CRUD DE APOYOS (Administrador)
# ===============================================
def listar_apoyos(request):
    apoyos = Apoyo.objects.all().order_by('-fecha_inicio')
    paginator = Paginator(apoyos, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'administrador/apoyos/listar_apoyos.html', {
        'page_obj': page_obj,
        'apoyos': page_obj
    })

def crear_apoyo(request):
    if request.method == 'POST':
        form = ApoyoForm(request.POST, request.FILES) 
        requisitos = request.POST.getlist('requisitos[]')
        if form.is_valid():
            apoyo = form.save()
            for req in requisitos:
                if req.strip():
                    Requisito.objects.create(apoyo=apoyo, descripcion=req.strip())
            messages.success(request, "Apoyo creado correctamente.")
            return redirect('listar_apoyos_admin')  # 👈 URL específica del admin
    else:
        form = ApoyoForm()
    return render(request, 'administrador/apoyos/crear_apoyo.html', {'form': form})

def editar_apoyo(request, apoyo_id):
    apoyo = get_object_or_404(Apoyo, id=apoyo_id)
    if request.method == 'POST':
        form = ApoyoForm(request.POST, request.FILES, instance=apoyo) 
        requisitos = request.POST.getlist('requisitos[]')
        if form.is_valid():
            form.save()
            apoyo.requisitos.all().delete()
            for req in requisitos:
                if req.strip():
                    Requisito.objects.create(apoyo=apoyo, descripcion=req.strip())
            messages.success(request, "Apoyo actualizado correctamente.")
            return redirect('listar_apoyos_admin')
        else:
            messages.error(request, "Por favor revisa los campos.")
    else:
        form = ApoyoForm(instance=apoyo)
    return render(request, 'administrador/apoyos/editar_apoyo.html', {
        'form': form,
        'apoyo': apoyo
    })

def eliminar_apoyo(request, apoyo_id):
    apoyo = get_object_or_404(Apoyo, id=apoyo_id)
    apoyo.delete()
    messages.success(request, "Apoyo eliminado correctamente.")
    return redirect('listar_apoyos_admin')

# ===============================================
# MÓDULO DE SOLICITUDES (Administrador)
# ===============================================
def listar_solicitudes_view(request):
    estado = request.GET.get('estado')
    search = request.GET.get('q')
    solicitudes = Solicitud.objects.select_related('usuario', 'apoyo')
    if estado in ['pendiente', 'aprobada', 'rechazada']:
        solicitudes = solicitudes.filter(estado=estado)
    if search:
        solicitudes = solicitudes.filter(
            Q(usuario__nombre__icontains=search) |
            Q(usuario__apellidos__icontains=search) |
            Q(apoyo__nombre__icontains=search)
        )
    paginator = Paginator(solicitudes, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'administrador/solicitudes/solicitudes.html', {
        'page_obj': page_obj,
        'solicitudes': page_obj,
        'estado': estado,
        'search': search,
    })

def detalle_solicitud_view(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    respuestas = solicitud.respuestas.select_related('pregunta')
    documentos = solicitud.documentos.select_related('requisito').all()
    modo_edicion = request.GET.get('editar') == '1'
    if request.method == 'POST':
        for doc in documentos:
            estado = request.POST.get(f'doc_estado_{doc.id}')
            observaciones = request.POST.get(f'doc_observaciones_{doc.id}', '').strip()
            if estado in dict(DocumentoRequisito.ESTADOS).keys():
                doc.estado = estado
                doc.observaciones = observaciones
                doc.save()
        accion = request.POST.get('accion')
        if accion == 'aprobar':
            solicitud.estado = 'aprobada'
            solicitud.save()
            messages.success(request, "La solicitud fue aprobada exitosamente.")
        elif accion == 'rechazar':
            motivo = request.POST.get('motivo_rechazo', '').strip()
            if not motivo:
                messages.error(request, "Debes ingresar un motivo para rechazar la solicitud.")
                return redirect('detalle_solicitud_admin', solicitud_id=solicitud.id)
            solicitud.estado = 'rechazada'
            solicitud.motivo_rechazo = motivo
            solicitud.save()
            messages.success(request, "La solicitud fue rechazada exitosamente.")
        return redirect('listar_solicitudes_admin')
    return render(request, 'administrador/solicitudes/detalle.html', {
        'solicitud': solicitud,
        'respuestas': respuestas,
        'documentos': documentos,
        'modo_edicion': modo_edicion
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from apoyos.models import Solicitud, DocumentoRequisito

# ===============================================
# MÓDULO DE SOLICITUDES DEL ADMINISTRADOR
# ===============================================

@login_required
def listar_solicitudes_admin(request):
    if request.user.rol != 'administrador':
        return redirect('panel_alcalde')  # redirigir si no es admin

    estado = request.GET.get('estado')
    search = request.GET.get('q')
    solicitudes = Solicitud.objects.select_related('usuario', 'apoyo')

    if estado in ['pendiente', 'aprobada', 'rechazada']:
        solicitudes = solicitudes.filter(estado=estado)

    if search:
        solicitudes = solicitudes.filter(
            Q(usuario__nombre__icontains=search) |
            Q(usuario__apellidos__icontains=search) |
            Q(apoyo__nombre__icontains=search)
        )

    paginator = Paginator(solicitudes, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'administrador/solicitudes/solicitudes.html', {
        'page_obj': page_obj,
        'solicitudes': page_obj,
        'estado': estado,
        'search': search,
    })


@login_required
def detalle_solicitud_admin(request, solicitud_id):
    if request.user.rol != 'administrador':
        return redirect('panel_alcalde')

    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    respuestas = solicitud.respuestas.select_related('pregunta')
    documentos = solicitud.documentos.select_related('requisito').all()
    modo_edicion = request.GET.get('editar') == '1'

    if request.method == 'POST':
        for doc in documentos:
            estado = request.POST.get(f'doc_estado_{doc.id}')
            observaciones = request.POST.get(f'doc_observaciones_{doc.id}', '').strip()
            if estado in dict(DocumentoRequisito.ESTADOS).keys():
                doc.estado = estado
                doc.observaciones = observaciones
                doc.save()

        accion = request.POST.get('accion')
        if accion == 'aprobar':
            solicitud.estado = 'aprobada'
            solicitud.save()
            messages.success(request, "La solicitud fue aprobada exitosamente.")
        elif accion == 'rechazar':
            motivo = request.POST.get('motivo_rechazo', '').strip()
            if not motivo:
                messages.error(request, "Debes ingresar un motivo para rechazar la solicitud.")
                return redirect('detalle_solicitud_admin', solicitud_id=solicitud.id)
            solicitud.estado = 'rechazada'
            solicitud.motivo_rechazo = motivo
            solicitud.save()
            messages.success(request, "La solicitud fue rechazada exitosamente.")
        return redirect('listar_solicitudes_admin')

    return render(request, 'administrador/solicitudes/detalle.html', {
        'solicitud': solicitud,
        'respuestas': respuestas,
        'documentos': documentos,
        'modo_edicion': modo_edicion
    })


@login_required
def editar_solicitud_admin(request, solicitud_id):
    if request.user.rol != 'administrador':
        return redirect('panel_alcalde')

    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    respuestas = solicitud.respuestas.select_related('pregunta')
    documentos = solicitud.documentos.select_related('requisito').all()
    modo_edicion = True

    if request.method == 'POST':
        for doc in documentos:
            estado = request.POST.get(f'doc_estado_{doc.id}')
            observaciones = request.POST.get(f'doc_observaciones_{doc.id}', '').strip()
            if estado in dict(DocumentoRequisito.ESTADOS).keys():
                doc.estado = estado
                doc.observaciones = observaciones
                doc.save()

        accion = request.POST.get('accion')
        if accion == 'aprobar':
            solicitud.estado = 'aprobada'
            solicitud.save()
            messages.success(request, "La solicitud fue aprobada exitosamente.")
        elif accion == 'rechazar':
            motivo = request.POST.get('motivo_rechazo', '').strip()
            if not motivo:
                messages.error(request, "Debes ingresar un motivo para rechazar la solicitud.")
                return redirect('editar_solicitud_admin', solicitud_id=solicitud.id)
            solicitud.estado = 'rechazada'
            solicitud.motivo_rechazo = motivo
            solicitud.save()
            messages.success(request, "La solicitud fue rechazada exitosamente.")
        return redirect('listar_solicitudes_admin')

    return render(request, 'administrador/solicitudes/editar_detalle.html', {
        'solicitud': solicitud,
        'respuestas': respuestas,
        'documentos': documentos,
        'modo_edicion': modo_edicion
    })

# ===============================================
# IMPORTACIONES
# ===============================================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.template.loader import get_template
from django.utils.timezone import now
from xhtml2pdf import pisa
from autenticacion.models import CustomUser
from autenticacion.forms import RegistroForm
from apoyos.models import Apoyo, DocumentoRequisito, QuejaSugerencia, Requisito, Solicitud
from apoyos.forms import ApoyoForm
from noticias.models import Noticia
from sugerencias.models import Sugerencia
from .forms import EditarAdministradorForm


# ===============================================
# DECORADORES
# ===============================================
def solo_alcalde(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.rol != 'alcalde':
            return HttpResponseForbidden("No tienes permiso para acceder a esta sección.")
        return view_func(request, *args, **kwargs)
    return wrapper


# ===============================================
# PANEL PRINCIPAL DEL ALCALDE
# ===============================================
@solo_alcalde
def panel_alcalde(request):
    return render(request, 'alcalde/panel.html')


# ===============================================
# CRUD DE ADMINISTRADORES
# ===============================================
@solo_alcalde
def listado_administradores_view(request):
    administradores = CustomUser.objects.filter(rol='administrador')
    return render(request, 'alcalde/administradores/panel_admin.html', {'administradores': administradores})


@solo_alcalde
def crear_administrador_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.rol = 'administrador'
            user.save()
            messages.success(request, "Administrador creado correctamente.")
            return redirect('listado_administradores')
        else:
            messages.error(request, "Ocurrió un error. Revisa los campos.")
    else:
        form = RegistroForm()
    return render(request, 'alcalde/administradores/crear_administrador.html', {'form': form})


@solo_alcalde
def editar_administrador_view(request, admin_id):
    admin = get_object_or_404(CustomUser, id=admin_id, rol='administrador')

    if request.method == 'POST':
        form = EditarAdministradorForm(request.POST, instance=admin)
        if form.has_changed():
            if form.is_valid():
                form.save()
                messages.success(request, "Administrador actualizado correctamente.")
                return redirect('listado_administradores')
            else:
                messages.error(request, "Hubo errores al actualizar el administrador.")
        else:
            messages.warning(request, "No realizaste ningún cambio.")
    else:
        form = EditarAdministradorForm(instance=admin)

    return render(request, 'alcalde/administradores/editar_administrador.html', {
        'form': form,
        'admin': admin
    })


@solo_alcalde
def eliminar_administrador_view(request, admin_id):
    admin = get_object_or_404(CustomUser, id=admin_id, rol='administrador')
    admin.delete()
    messages.success(request, "Administrador eliminado correctamente.")
    return redirect('listado_administradores')


# ===============================================
# CRUD DE APOYOS
# ===============================================
@solo_alcalde
def listar_apoyos(request):
    apoyos = Apoyo.objects.all().order_by('-fecha_inicio')
    paginator = Paginator(apoyos, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'alcalde/apoyos/listar_apoyos.html', {
        'page_obj': page_obj,
        'apoyos': page_obj
    })


@solo_alcalde
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
            return redirect('listar_apoyos')
    else:
        form = ApoyoForm()

    return render(request, 'alcalde/apoyos/crear_apoyo.html', {'form': form})


@solo_alcalde
def editar_apoyo(request, apoyo_id):
    apoyo = get_object_or_404(Apoyo, id=apoyo_id)

    if request.method == 'POST':
        form = ApoyoForm(request.POST, request.FILES, instance=apoyo, editar=True)  # 👈 AQUI
        requisitos = request.POST.getlist('requisitos[]')

        if form.is_valid():
            form.save()
            apoyo.requisitos.all().delete()
            for req in requisitos:
                if req.strip():
                    Requisito.objects.create(apoyo=apoyo, descripcion=req.strip())
            messages.success(request, "Apoyo actualizado correctamente.")
            return redirect('listar_apoyos')
        else:
            messages.error(request, "Por favor revisa los campos.")
    else:
        form = ApoyoForm(instance=apoyo, editar=True)  # 👈 AQUI también

    return render(request, 'alcalde/apoyos/editar_apoyo.html', {
        'form': form,
        'apoyo': apoyo
    })


@solo_alcalde
def eliminar_apoyo(request, apoyo_id):
    apoyo = get_object_or_404(Apoyo, id=apoyo_id)
    apoyo.delete()
    messages.success(request, "Apoyo eliminado correctamente.")
    return redirect('listar_apoyos')


# ===============================================
# MÓDULO DE SOLICITUDES DEL ALCALDE
# ===============================================

@solo_alcalde
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

    return render(request, 'alcalde/solicitudes/solicitudes.html', {
        'page_obj': page_obj,
        'solicitudes': page_obj,
        'estado': estado,
        'search': search,
    })


@solo_alcalde
def detalle_solicitud_alcalde(request, solicitud_id):
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
                return redirect('detalle_solicitud_alcalde', solicitud_id=solicitud.id)
            solicitud.estado = 'rechazada'
            solicitud.motivo_rechazo = motivo
            solicitud.save()
            messages.success(request, "La solicitud fue rechazada exitosamente.")
        return redirect('solicitudes_alcalde')

    return render(request, 'alcalde/solicitudes/detalle.html', {
        'solicitud': solicitud,
        'respuestas': respuestas,
        'documentos': documentos,
        'modo_edicion': modo_edicion
    })


@solo_alcalde
def editar_solicitud_alcalde(request, solicitud_id):
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
                return redirect('editar_solicitud_alcalde', solicitud_id=solicitud.id)
            solicitud.estado = 'rechazada'
            solicitud.motivo_rechazo = motivo
            solicitud.save()
            messages.success(request, "La solicitud fue rechazada exitosamente.")
        return redirect('solicitudes_alcalde')

    return render(request, 'alcalde/solicitudes/editar_detalle.html', {
        'solicitud': solicitud,
        'respuestas': respuestas,
        'documentos': documentos,
        'modo_edicion': modo_edicion
    })


# ===============================================
# ESTADÍSTICAS DE APOYOS MÁS SOLICITADOS
# ===============================================
@solo_alcalde
def apoyos_mas_solicitados(request):
    apoyos_solicitados = (
        Apoyo.objects.annotate(total_solicitudes=Count('solicitud'))
        .order_by('-total_solicitudes')
    )
    return render(request, 'alcalde/estadisticas/apoyos_mas_solicitados.html', {
        'apoyos_solicitados': apoyos_solicitados
    })


@solo_alcalde
def apoyos_mas_solicitados_view(request):
    apoyos_solicitados = Apoyo.objects.annotate(
       total_solicitudes=Count('solicitud')
    ).order_by('-total_solicitudes')

    solicitantes_por_apoyo = {}
    for apoyo in apoyos_solicitados:
        solicitantes = Solicitud.objects.filter(apoyo=apoyo).select_related('usuario')
        solicitantes_por_apoyo[apoyo.id] = [{
            'nombre': s.usuario.nombre + ' ' + s.usuario.apellidos,
            'telefono': s.usuario.telefono,
            'email': s.usuario.email,
            'estado': s.estado,
        } for s in solicitantes]

    return render(request, 'alcalde/estadisticas/apoyos_mas_solicitados.html', {
        'apoyos_solicitados': apoyos_solicitados,
        'solicitantes_por_apoyo': solicitantes_por_apoyo
    })


@solo_alcalde
def generar_pdf_apoyo(request, apoyo_id):
    apoyo = get_object_or_404(Apoyo, id=apoyo_id)
    solicitudes = Solicitud.objects.filter(apoyo=apoyo).select_related('usuario')

    template_path = 'alcalde/estadisticas/pdf_apoyo.html'
    context = {
        'apoyo': apoyo,
        'solicitudes': solicitudes,
        'now': now(),
    }
    response = HttpResponse(content_type='application/pdf')
    nombre_limpio = apoyo.nombre.replace(" ", "_").replace("/", "-")
    response['Content-Disposition'] = f'attachment; filename="reporte_{nombre_limpio}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
    return response


@solo_alcalde
def generar_pdf_apoyos_totales(request):
    apoyos_solicitados = Apoyo.objects.annotate(total_solicitudes=Count('solicitud')).order_by('-total_solicitudes')
    total_solicitudes = sum([a.total_solicitudes for a in apoyos_solicitados])

    template_path = 'alcalde/estadisticas/pdf_apoyos_general.html'
    context = {
        'apoyos_solicitados': apoyos_solicitados,
        'total_solicitudes': total_solicitudes,
        'now': now(),
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_apoyos_mas_solicitados.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
    return response


# ===============================================
# SUGERENCIAS / QUEJAS
# ===============================================
@solo_alcalde
def listar_sugerencias_view(request):
    tipo = request.GET.get('tipo')
    sugerencias = Sugerencia.objects.select_related('usuario').order_by('-fecha_creacion')

    if tipo in ['queja', 'sugerencia']:
        sugerencias = sugerencias.filter(tipo=tipo)

    paginator = Paginator(sugerencias, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'alcalde/sugerencias/listar.html', {
        'page_obj': page_obj,
        'tipo_actual': tipo
    })

# ===============================================
# nuneros
# ===============================================

@solo_alcalde
def panel_alcalde(request):
    solicitudes_recibidas = Solicitud.objects.count()
    apoyos_activos = Apoyo.objects.filter(disponible=True).count()
    quejas_sugerencias = Sugerencia.objects.count()  # <-- esto debe estar
    noticias_publicadas = Noticia.objects.count()

    return render(request, 'alcalde/panel.html', {
        'solicitudes_recibidas': solicitudes_recibidas,
        'apoyos_activos': apoyos_activos,
        'quejas_sugerencias': quejas_sugerencias,  # <-- esto también
        'noticias_publicadas': noticias_publicadas,
    })


from django.http import HttpResponse
import openpyxl
from openpyxl.styles import Font
from io import BytesIO
from apoyos.models import Solicitud  # Ajusta según tu estructura de proyecto

def exportar_excel_solicitudes(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Solicitudes"

    # Encabezados
    encabezados = [
        'Nombre', 'CURP', 'Correo', 'Teléfono', 'Municipio', 'Código Postal',
        'Apoyo', 'Tipo', 'Estado', 'Fecha Solicitud', 'Motivo Rechazo',
        'Situación', 'Ocupación', 'Educación', 'Vivienda',
        'Mayor de Edad', 'Condiciones Aceptadas',
        'Clave Elector', 'Sección', 'Vigencia INE'
    ]
    ws.append(encabezados)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    # Consultar solicitudes
    solicitudes = Solicitud.objects.select_related('usuario', 'apoyo', 'apoyo__tipo')

    for s in solicitudes:
        ws.append([
            f"{s.usuario.nombre} {s.usuario.apellidos}",
            s.usuario.curp,
            s.usuario.email,
            s.usuario.telefono,
            str(s.usuario.municipio),  # 🔧 Aquí está el fix
            s.usuario.codigo_postal,
            s.apoyo.nombre,
            s.apoyo.tipo.nombre,
            s.estado,
            s.fecha_solicitud.strftime('%d/%m/%Y %H:%M'),
            s.motivo_rechazo if s.estado == 'rechazada' else '',
            s.situacion or '',
            s.ocupacion or '',
            s.educacion or '',
            s.vivienda or '',
            'Sí' if s.mayor_edad else 'No',
            'Sí' if s.condiciones else 'No',
            s.clave_elector or '',
            s.seccion or '',
            s.vigencia or ''
        ])

    # Preparar respuesta
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=\"solicitudes_completas.xlsx\"'

    wb.save(response)
    return response


from django.shortcuts import render, redirect, get_object_or_404
from apoyos.models import Banner
from apoyos.forms import BannerForm
from django.contrib.auth.decorators import user_passes_test

def es_admin_o_alcalde(user):
    return user.rol in ['administrador', 'alcalde']

@user_passes_test(es_admin_o_alcalde)
def lista_banners(request):
    banners = Banner.objects.all()
    return render(request, 'banners/lista.html', {'banners': banners})

@user_passes_test(es_admin_o_alcalde)
def crear_banner(request):
    form = BannerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('lista_banners')
    return render(request, 'banners/form.html', {'form': form})

@user_passes_test(es_admin_o_alcalde)
def eliminar_banner(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    banner.delete()
    return redirect('lista_banners')

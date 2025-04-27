from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Noticia
from .forms import NoticiaForm

# =====================================================
# ADMINISTRADOR / ALCALDE: Validación directa por rol
# =====================================================

def listar_noticias(request):
    if not request.user.is_authenticated or request.user.rol not in ['alcalde', 'administrador']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta sección.")
    
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')
    return render(request, 'noticias/listar.html', {'noticias': noticias})

def crear_noticia(request):
    if not request.user.is_authenticated or request.user.rol not in ['alcalde', 'administrador']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta sección.")

    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_noticias')
    else:
        form = NoticiaForm()
    return render(request, 'noticias/crear.html', {'form': form})

def editar_noticia(request, noticia_id):
    if not request.user.is_authenticated or request.user.rol not in ['alcalde', 'administrador']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta sección.")

    noticia = get_object_or_404(Noticia, id=noticia_id)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('listar_noticias')
    else:
        form = NoticiaForm(instance=noticia)
    return render(request, 'noticias/editar.html', {'form': form, 'noticia': noticia})

def eliminar_noticia(request, noticia_id):
    if not request.user.is_authenticated or request.user.rol not in ['alcalde', 'administrador']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta sección.")

    noticia = get_object_or_404(Noticia, id=noticia_id)
    noticia.delete()
    return redirect('listar_noticias')


# =====================================================
# USUARIOS (Vista pública)
# =====================================================

def listar_noticias_usuario(request):
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')
    return render(request, 'usuario/listar.html', {'noticias': noticias})

def detalle_noticia_usuario(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    return render(request, 'usuario/detalle.html', {'noticia': noticia})



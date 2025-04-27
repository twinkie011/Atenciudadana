from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SugerenciaForm

@login_required
def enviar_sugerencia(request):
    if request.method == 'POST':
        form = SugerenciaForm(request.POST)
        if form.is_valid():
            sugerencia = form.save(commit=False)
            sugerencia.usuario = request.user
            sugerencia.save()
            messages.success(request, 'Gracias por tu mensaje. Ha sido enviado exitosamente.')
            return redirect('panel_usuario')
    else:
        form = SugerenciaForm()
    return render(request, 'sugerencias/enviar_sugerencia.html', {'form': form})

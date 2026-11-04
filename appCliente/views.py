from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Estado, Estado_Activo, ForeignKey

# Create your views here.

def inicio(request: HttpRequest) -> HttpResponse:
    estado: Estado | ForeignKey
    estado_activo: Estado_Activo | None = Estado_Activo.objects.first()

    if estado_activo is None:
        estado = get_object_or_404(Estado, numero_etapa=1)

        nuevo_estado_activo: Estado_Activo = Estado_Activo(estado_id=estado)
        nuevo_estado_activo.save()

    else:
        estado = estado_activo.estado_id


    contexto: dict[Any, Any] = {
        'estado_activo': estado
    }

    return render(request=request, template_name='inicio.html', context=contexto)

def login_page(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username: str | None | object = request.POST.get(key='username', default=None)
        password: str | None | object = request.POST.get(key='password', default=None)

        user: User | None = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print('USER AUTENTIFICATED')
            return redirect('admin_page')
        else:
            print('NOT USER AUTENTIFICATED')

    return render(request=request, template_name='login.html')

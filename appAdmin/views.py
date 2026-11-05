from typing import Any

from django.db.models import ForeignKey
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from appCliente.models import Estado, Estado_Activo

# Create your views here.


def cambio_etapas(request: HttpRequest) -> HttpResponse:
    estado: Estado | ForeignKey

    # Obtener estado activo
    estado_activo: Estado_Activo | None = Estado_Activo.objects.first()

    # Si o si va a haber un estado activo
    assert estado_activo
    estado = estado_activo.estado_id


    contexto: dict[Any, Any] = {
        'estado_activo':    estado,
        'estado_siguiente': estado,
        'estado_anterior':  estado,
    }

    return render(request=request, template_name='cambio_etapas.html', context=contexto)


def editor_etapas(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name='editor_etapas.html')


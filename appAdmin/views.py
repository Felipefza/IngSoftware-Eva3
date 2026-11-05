from typing import Any

from django.db.models import ForeignKey
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from appCliente.models import Estado, Estado_Activo

# Create your views here.


def cambio_etapas(request: HttpRequest) -> HttpResponse:
    estado: Estado | ForeignKey
    estado_activo: Estado_Activo | None = Estado_Activo.objects.first()

    if estado_activo is None:
        estado = get_object_or_404(Estado, numero_etapa=1)

        nuevo_estado_activo: Estado_Activo = Estado_Activo(estado_id=estado)
        nuevo_estado_activo.save()

    else:
        estado = estado_activo.estado_id


    contexto: dict[Any, Any] = {
        'estado_activo':    estado,
        'estado_siguiente': estado,
        'estado_anterior':  estado,
    }

    return render(request=request, template_name='cambio_etapas.html', context=contexto)


def editor_etapas(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name='editor_etapas.html')


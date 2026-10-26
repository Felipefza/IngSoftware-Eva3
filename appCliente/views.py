from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

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

from typing import Any

from django.db.models import ForeignKey
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from appCliente.models import Estado, Estado_Activo

# Create your views here.


def cambio_etapas(request: HttpRequest) -> HttpResponse:
    estado_activo: Estado_Activo | None = Estado_Activo.objects.first()

    estado:           Estado
    estado_siguiente: Estado
    estado_anterior:  Estado

    try:
        assert      estado_activo, 'Estado activo es nulo'
        assert type(estado_activo.estado_id) == Estado, 'estado_id no es Estado'

        estado = estado_activo.estado_id

    except AssertionError as e:
        print(f'AssertionError {e}')
        return redirect('editor_etapas_page')

    # COMIENZO DEL POST

    if request.method == 'POST':
        etapa: int | None | object = request.POST.get(key='etapa', default=None)
        etapa_estado: Estado | None = Estado.objects.filter(pk=etapa).first()

        try:
            assert type(etapa_estado) == Estado, 'etapa no es Estado'

            estado_activo.delete()

            estado_activo = Estado_Activo(estado_id=etapa_estado)
            estado_activo.save()

            assert type(estado_activo.estado_id) == Estado, 'estado_id no es Estado'
            estado = estado_activo.estado_id

        except AssertionError as e:
            print(f'AssertionError {e}')

    # FIN DEL POST

    # COMIENZO DEL GET

    cantidad_estados: int = Estado.objects.all().count()

    if cantidad_estados == 0:
        return redirect('editor_etapas_page')

    if cantidad_estados == 1:
        estado_siguiente = estado
        estado_anterior  = estado

    else:
        estado_id:           int = estado.id
        estado_siguiente_id: int = estado_id + 1
        estado_anterior_id:  int = estado_id - 1

        nuevo_estado_siguiente: Estado | None = Estado.objects.filter(id=estado_siguiente_id).first()
        nuevo_estado_anterior:  Estado | None = Estado.objects.filter(id=estado_anterior_id ).first()

        if nuevo_estado_siguiente is None:
            estado_siguiente = Estado.objects.first()
        else:
            estado_siguiente = nuevo_estado_siguiente


        if nuevo_estado_anterior is None:
            estado_anterior = Estado.objects.last()
        else:
            estado_anterior = nuevo_estado_anterior


    contexto: dict[Any, Any] = {
        'estado_activo':    estado,
        'estado_siguiente': estado_siguiente,
        'estado_anterior':  estado_anterior,
    }

    return render(request=request, template_name='cambio_etapas.html', context=contexto)


def editor_etapas(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name='editor_etapas.html')


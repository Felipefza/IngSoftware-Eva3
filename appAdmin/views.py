import logging
from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from appAdmin.forms import Estado_Form
from appCliente.models import Estado, Estado_Activo

logger = logging.getLogger(__name__)


def cambio_etapas(request: HttpRequest) -> HttpResponse:
  estado_activo: Estado_Activo | None = Estado_Activo.objects.first()

  estado: Estado
  estado_siguiente: Estado
  estado_anterior: Estado

  try:
    assert estado_activo, 'Estado activo es nulo'
    assert isinstance(estado_activo.estado_id, Estado), 'estado_id no es Estado'
    estado = estado_activo.estado_id
  except AssertionError as e:
    logger.error(f'AssertionError en cambio_etapas (GET): {e}')
    return redirect('editor_etapas_page')

  # COMIENZO DEL POST
  if request.method == 'POST':
    etapa_id = request.POST.get(key='etapa', default=None)
    etapa_estado: Estado | None = Estado.objects.filter(pk=etapa_id).first()

    try:
      assert isinstance(etapa_estado, Estado), 'etapa no es Estado'

      Estado_Activo.objects.all().delete()
      nuevo_activo = Estado_Activo(estado_id=etapa_estado)
      nuevo_activo.save()

      logger.info(
          f'Etapa cambiada exitosamente a: {etapa_estado.titulo_estado}'
      )
    except AssertionError as e:
      logger.error(f'AssertionError en cambio_etapas (POST): {e}')

    return redirect(
        'cambio_etapas_page'
    )

  # COMIENZO DEL GET
  cantidad_estados: int = Estado.objects.count()

  if cantidad_estados == 0:
    return redirect('editor_etapas_page')

  if cantidad_estados == 1:
    estado_siguiente = estado
    estado_anterior = estado
  else:
    actual_id: int = estado.id
    estado_siguiente = (
        Estado.objects.filter(id__gt=actual_id).order_by('id').first()
        or Estado.objects.first()
    )
    estado_anterior = (
        Estado.objects.filter(id__lt=actual_id).order_by('-id').first()
        or Estado.objects.last()
    )

  contexto: dict[str, Any] = {
      'estado_activo': estado,
      'estado_siguiente': estado_siguiente,
      'estado_anterior': estado_anterior,
  }

  return render(request=request, template_name='cambio_etapas.html', context=contexto)


def editor_etapas(request: HttpRequest) -> HttpResponse:
  estados = Estado.objects.all().order_by('numero_etapa')
  etapa_activa = Estado_Activo.objects.all().first()
  contexto = {'estados': estados, 'etapa_activa': etapa_activa}
  return render(request=request, template_name='editor_etapas.html', context=contexto)


def crear_etapa(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        estado_form: Estado_Form = Estado_Form(request.POST)
        if estado_form.is_valid():
            estado_form.save()
        else:
            estado_form = Estado_Form()
            return render(request, 'crear_etapa.html')

        return redirect('editor_etapas_page')
    return render(request, 'crear_etapa.html')


def modificar_etapa(request: HttpRequest) -> HttpResponse:
    pk: int | None | object
    estado_cambiar: Estado
    contexto = {}

    if request.method == 'GET':
        pk = request.GET.get('pk')

        if pk is None:
            return redirect('editor_etapas_page')

        estado_cambiar = Estado.objects.get(pk=pk)
        contexto['estado'] = estado_cambiar


    if request.method == 'POST':
        pk = request.POST.get('pk')

        if pk is None:
            return redirect('editor_etapas_page')

        estado_cambiar = Estado.objects.get(pk=pk)
        contexto['estado'] = estado_cambiar

        estado_form: Estado_Form = Estado_Form(data=request.POST, instance=estado_cambiar)

        if estado_form.is_valid():
            estado_form.save()
        else:
            estado_form = Estado_Form()
            return render(request, 'modificar_etapa.html', contexto)

        return redirect('editor_etapas_page')
    return render(request, 'modificar_etapa.html', contexto)

def eliminar_etapa(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        estado_cantidad: int = Estado.objects.count()

        if estado_cantidad < 2:
            return redirect('editor_etapas_page')

        num = request.POST.get('numero_etapa')

        if num is None:
            return redirect('editor_etapas_page')

        etapa_a_eliminar: Estado = Estado.objects.get(numero_etapa=num)
        etapa_a_eliminar.delete()

    return redirect('editor_etapas_page')

"""
URL configuration for panaderia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from appAdmin.views import cambio_etapas, editor_etapas, eliminar_etapa, modificar_etapa

urlpatterns = [
    path(route='cambio-etapas', view=cambio_etapas, name='cambio_etapas_page'),
    path(route='editor-etapas', view=editor_etapas, name='editor_etapas_page'),
    path(route='modificar-etapa', view=modificar_etapa, name='modificar_etapa'),
    path(route='eliminar-etapa',  view=eliminar_etapa, name='eliminar_etapa'),
]

from django.forms import ModelForm

from appCliente.models import Estado


class Estado_Form(ModelForm):
    class Meta:
        model = Estado
        fields = ['numero_etapa', 'titulo_estado', 'descripcion_estado']

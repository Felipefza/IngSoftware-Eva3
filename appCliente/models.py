from django.db.models import (
    CASCADE,
    AutoField,
    ForeignKey,
    IntegerField,
    Manager,
    Model,
    TextField,
)

# Create your models here.


class Estado(Model):
    id = AutoField(primary_key=True)
    numero_etapa = IntegerField(null=False)
    titulo_estado = TextField(null=False)
    descripcion_estado = TextField(null=False)

    objects: Manager = Manager()

    def __str__(self):
        return (
            f'\n ==== ID {self.id}===='
            f'\n N° Etapa:      {self.numero_etapa}'
            f'\n Titulo:        {self.titulo_estado}'
            f'\n Descripción:   {self.descripcion_estado}'
            f'\n'
        )


class Estado_Activo(Model):
    id = AutoField(primary_key=True)
    estado_id = ForeignKey(to=Estado, on_delete=CASCADE)

    objects: Manager = Manager()

    def __str__(self):
        return (
            f'\n ==== ID {self.id}===='
            f'\n Estado ID:     {self.estado_id}'
            f'\n'
        )

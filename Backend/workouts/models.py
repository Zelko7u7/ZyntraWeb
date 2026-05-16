import uuid
from django.db import models

class Rutina(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    objetivo = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50)
    duracion_min = models.IntegerField()

    def __str__(self):
        return self.nombre


class Ejercicio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    grupo_muscular = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class RutinaEjercicio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    orden = models.IntegerField()
    series = models.IntegerField()
    repeticiones = models.IntegerField()


class Entrenamiento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey("users.Usuario", on_delete=models.CASCADE)
    rutina = models.ForeignKey(Rutina, on_delete=models.SET_NULL, null=True)

    fecha = models.DateTimeField()
    duracion = models.IntegerField()
    calorias = models.FloatField()
    estado = models.CharField(max_length=50)
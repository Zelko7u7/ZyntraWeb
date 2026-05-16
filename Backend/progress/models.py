import uuid
from django.db import models

class Nivel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero = models.IntegerField()
    xp_requerida = models.IntegerField()


class Rango(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    xp_min = models.IntegerField()
    xp_max = models.IntegerField()


class Progreso(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    usuario = models.ForeignKey("users.Usuario", on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.SET_NULL, null=True)
    rango = models.ForeignKey(Rango, on_delete=models.SET_NULL, null=True)

    xp_total = models.IntegerField()
    racha_actual = models.IntegerField()
    mejor_racha = models.IntegerField()

    calorias_totales = models.IntegerField()
    entrenamientos = models.IntegerField()
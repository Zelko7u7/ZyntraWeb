import uuid
from django.db import models

class PlanNutricional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    calorias = models.IntegerField()
    proteinas = models.IntegerField()
    carbs = models.IntegerField()
    grasas = models.IntegerField()


class RegistroComida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    usuario = models.ForeignKey("users.Usuario", on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanNutricional, on_delete=models.SET_NULL, null=True)

    fecha = models.DateTimeField()
    calorias = models.IntegerField()
    proteinas = models.IntegerField()
    carbs = models.IntegerField()
    grasas = models.IntegerField()
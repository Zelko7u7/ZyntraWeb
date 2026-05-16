import uuid
from django.db import models

class Logro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    xp = models.IntegerField()


class LogroUsuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    usuario = models.ForeignKey("users.Usuario", on_delete=models.CASCADE)
    logro = models.ForeignKey(Logro, on_delete=models.CASCADE)

    fecha = models.DateTimeField(auto_now_add=True)
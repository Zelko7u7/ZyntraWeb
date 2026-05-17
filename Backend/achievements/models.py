import uuid
from django.db import models


class Logro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        "users.Usuario",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="logros_creados",
    )
    nombre = models.CharField(max_length=100)
    xp = models.IntegerField()

    def __str__(self):
        return self.nombre


class LogroUsuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    usuario = models.ForeignKey(
        "users.Usuario",
        on_delete=models.CASCADE,
        related_name="logros_desbloqueados",
    )
    logro = models.ForeignKey(
        Logro,
        on_delete=models.CASCADE,
        related_name="desbloqueos",
    )

    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "logro")

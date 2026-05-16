import uuid
from django.db import models

class ChatConversacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey("users.Usuario", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)


class ChatMensaje(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversacion = models.ForeignKey(ChatConversacion, on_delete=models.CASCADE)

    rol = models.CharField(max_length=20)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
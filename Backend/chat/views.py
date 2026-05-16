from rest_framework import viewsets
from .models import ChatConversacion, ChatMensaje
from .serializers import *


class ChatConversacionViewSet(viewsets.ModelViewSet):
    queryset = ChatConversacion.objects.all()
    serializer_class = ChatConversacionSerializer


class ChatMensajeViewSet(viewsets.ModelViewSet):
    queryset = ChatMensaje.objects.all()
    serializer_class = ChatMensajeSerializer


class ChatConversacionViewSet(viewsets.ModelViewSet):
    queryset = ChatConversacion.objects.all()
    serializer_class = ChatConversacionSerializer

    def get_queryset(self):
        return ChatConversacion.objects.filter(
            usuario__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            usuario=self.request.user.usuario
        )
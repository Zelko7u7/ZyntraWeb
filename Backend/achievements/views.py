from rest_framework import viewsets
from .models import Logro, LogroUsuario
from .serializers import *


class LogroViewSet(viewsets.ModelViewSet):
    queryset = Logro.objects.all()
    serializer_class = LogroSerializer


#class LogroUsuarioViewSet(viewsets.ModelViewSet):
#    queryset = LogroUsuario.objects.all()
#    serializer_class = LogroUsuarioSerializer


class LogroUsuarioViewSet(viewsets.ModelViewSet):
    queryset = LogroUsuario.objects.all()
    serializer_class = LogroUsuarioSerializer

    def get_queryset(self):
        return LogroUsuario.objects.filter(
            usuario__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            usuario=self.request.user.usuario
        )
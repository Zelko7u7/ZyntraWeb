from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from .models import Rutina, Ejercicio, RutinaEjercicio, Entrenamiento
from .serializers import *


class RutinaViewSet(viewsets.ModelViewSet):
    queryset = Rutina.objects.all()
    serializer_class = RutinaSerializer

    def get_queryset(self):
        perfil = getattr(self.request.user, "usuario", None)
        if perfil is None:
            return Rutina.objects.none()
        return Rutina.objects.filter(usuario=perfil)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user.usuario)

    def perform_update(self, serializer):
        if serializer.instance.usuario_id != self.request.user.usuario.id:
            raise PermissionDenied("No puedes modificar esta rutina.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.usuario_id != self.request.user.usuario.id:
            raise PermissionDenied("No puedes eliminar esta rutina.")
        instance.delete()


class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer


class RutinaEjercicioViewSet(viewsets.ModelViewSet):
    queryset = RutinaEjercicio.objects.all()
    serializer_class = RutinaEjercicioSerializer


class EntrenamientoViewSet(viewsets.ModelViewSet):
    queryset = Entrenamiento.objects.all()
    serializer_class = EntrenamientoSerializer

    def get_queryset(self):
        return Entrenamiento.objects.filter(
            usuario__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            usuario=self.request.user.usuario
        )

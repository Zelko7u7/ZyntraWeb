from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Logro, LogroUsuario
from .serializers import LogroSerializer, LogroUsuarioSerializer


class LogroViewSet(viewsets.ModelViewSet):
    serializer_class = LogroSerializer
    queryset = Logro.objects.all()

    def get_queryset(self):
        perfil = getattr(self.request.user, "usuario", None)
        if perfil is None:
            return Logro.objects.none()
        return Logro.objects.filter(usuario=perfil).order_by("nombre")

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user.usuario)

    def perform_update(self, serializer):
        if serializer.instance.usuario_id != self.request.user.usuario.id:
            raise PermissionDenied("No puedes modificar este logro.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.usuario_id != self.request.user.usuario.id:
            raise PermissionDenied("No puedes eliminar este logro.")
        instance.delete()

    @action(detail=True, methods=["post"])
    def unlock(self, request, pk=None):
        logro = self.get_object()
        perfil = request.user.usuario
        lu, created = LogroUsuario.objects.get_or_create(
            usuario=perfil, logro=logro
        )
        serializer = LogroUsuarioSerializer(lu)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def lock(self, request, pk=None):
        logro = self.get_object()
        perfil = request.user.usuario
        LogroUsuario.objects.filter(usuario=perfil, logro=logro).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogroUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = LogroUsuarioSerializer
    queryset = LogroUsuario.objects.all()

    def get_queryset(self):
        perfil = getattr(self.request.user, "usuario", None)
        if perfil is None:
            return LogroUsuario.objects.none()
        return (
            LogroUsuario.objects
            .filter(usuario=perfil)
            .select_related("logro")
            .order_by("-fecha")
        )

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user.usuario)

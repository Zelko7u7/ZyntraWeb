from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from .models import PlanNutricional, RegistroComida
from .serializers import PlanNutricionalSerializer, RegistroComidaSerializer


class PlanNutricionalViewSet(viewsets.ModelViewSet):
    queryset = PlanNutricional.objects.all()
    serializer_class = PlanNutricionalSerializer

    def get_queryset(self):
        perfil = getattr(self.request.user, "usuario", None)
        if perfil is None:
            return PlanNutricional.objects.none()
        return PlanNutricional.objects.filter(usuario=perfil)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user.usuario)

    def perform_update(self, serializer):
        if serializer.instance.usuario_id != self.request.user.usuario.id:
            raise PermissionDenied("No puedes modificar este plan.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.usuario_id != self.request.user.usuario.id:
            raise PermissionDenied("No puedes eliminar este plan.")
        instance.delete()


class RegistroComidaViewSet(viewsets.ModelViewSet):
    queryset = RegistroComida.objects.all()
    serializer_class = RegistroComidaSerializer

    def get_queryset(self):
        return RegistroComida.objects.filter(
            usuario__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            usuario=self.request.user.usuario
        )

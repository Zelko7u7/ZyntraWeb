from rest_framework import viewsets
from .models import PlanNutricional, RegistroComida
from .serializers import *


class PlanNutricionalViewSet(viewsets.ModelViewSet):
    queryset = PlanNutricional.objects.all()
    serializer_class = PlanNutricionalSerializer


class RegistroComidaViewSet(viewsets.ModelViewSet):
    queryset = RegistroComida.objects.all()
    serializer_class = RegistroComidaSerializer


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
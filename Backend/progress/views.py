from rest_framework import viewsets
from .models import Nivel, Rango, Progreso
from .serializers import *


class NivelViewSet(viewsets.ModelViewSet):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer


class RangoViewSet(viewsets.ModelViewSet):
    queryset = Rango.objects.all()
    serializer_class = RangoSerializer


class ProgresoViewSet(viewsets.ModelViewSet):
    queryset = Progreso.objects.all()
    serializer_class = ProgresoSerializer


class ProgresoViewSet(viewsets.ModelViewSet):
    queryset = Progreso.objects.all()
    serializer_class = ProgresoSerializer

    def get_queryset(self):
        return Progreso.objects.filter(
            usuario__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            usuario=self.request.user.usuario
        )
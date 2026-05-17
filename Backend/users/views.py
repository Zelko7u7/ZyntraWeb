from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

from .models import Usuario, Avatar
from .serializers import UsuarioSerializer, AvatarSerializer, RegisterSerializer
from achievements.models import Logro, LogroUsuario


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        usuario = request.user.usuario
        serializer = self.get_serializer(usuario)
        return Response(serializer.data)


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        try:
            perfil = Usuario.objects.get(user=user)
            logro_inicio = Logro.objects.filter(
                nombre="Iniciar cuenta",
                usuario__isnull=True,
            ).first()
            if logro_inicio:
                LogroUsuario.objects.get_or_create(
                    usuario=perfil,
                    logro=logro_inicio,
                )
        except Usuario.DoesNotExist:
            pass

        return data


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

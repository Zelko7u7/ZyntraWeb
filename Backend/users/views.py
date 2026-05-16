from rest_framework import viewsets
from .models import Usuario, Avatar
from .serializers import UsuarioSerializer, AvatarSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from achievements.models import Logro, LogroUsuario
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Usuario

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        usuario = request.user.usuario
        serializer = self.get_serializer(usuario)
        return Response(serializer.data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,) # Cualquiera puede registrarse
    serializer_class = RegisterSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Ejecuta la validación normal (verifica usuario y contraseña)
        data = super().validate(attrs)
        
        # ¡Si llegamos aquí, el login fue exitoso! 
        user = self.user
        
        try:
            # Buscamos su perfil de atleta
            perfil = Usuario.objects.get(user=user)
            
            # ¡AQUÍ ESTÁ EL CAMBIO! Usamos el nombre exacto de tu base de datos
            logro_inicio = Logro.objects.filter(nombre="Iniciar cuenta").first()
            
            if logro_inicio:
                # get_or_create verifica si ya lo tiene. Si no lo tiene, se lo da.
                LogroUsuario.objects.get_or_create(
                    usuario=perfil, 
                    logro=logro_inicio
                )
        except Usuario.DoesNotExist:
            pass
            
        return data

# 2. Creamos la Vista que usa nuestro Serializador
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
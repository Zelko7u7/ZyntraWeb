from rest_framework import serializers
from .models import Logro, LogroUsuario


class LogroSerializer(serializers.ModelSerializer):
    desbloqueado = serializers.SerializerMethodField()

    class Meta:
        model = Logro
        fields = ["id", "nombre", "xp", "usuario", "desbloqueado"]
        read_only_fields = ["usuario"]

    def get_desbloqueado(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        perfil = getattr(request.user, "usuario", None)
        if perfil is None:
            return False
        return LogroUsuario.objects.filter(usuario=perfil, logro=obj).exists()


class LogroUsuarioSerializer(serializers.ModelSerializer):
    logro_nombre = serializers.CharField(source="logro.nombre", read_only=True)
    logro_xp = serializers.IntegerField(source="logro.xp", read_only=True)

    class Meta:
        model = LogroUsuario
        fields = ["id", "usuario", "logro", "logro_nombre", "logro_xp", "fecha"]
        read_only_fields = ["usuario", "fecha"]

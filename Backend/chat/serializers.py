from rest_framework import serializers
from .models import ChatConversacion, ChatMensaje


class ChatConversacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatConversacion
        fields = '__all__'
        read_only_fields = ['usuario']


class ChatMensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMensaje
        fields = '__all__'
        read_only_fields = ['fecha']


class EnviarMensajeSerializer(serializers.Serializer):
    mensaje = serializers.CharField(min_length=1, max_length=4000, trim_whitespace=True)
    conversacion_id = serializers.UUIDField(required=False, allow_null=True)

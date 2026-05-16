from rest_framework import serializers
from .models import ChatConversacion, ChatMensaje


class ChatConversacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatConversacion
        fields = '__all__'


class ChatMensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMensaje
        fields = '__all__'
from django.contrib import admin
from .models import ChatConversacion, ChatMensaje


@admin.register(ChatConversacion)
class ChatConversacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo')


@admin.register(ChatMensaje)
class ChatMensajeAdmin(admin.ModelAdmin):
    list_display = ('conversacion', 'rol', 'fecha')
    list_filter = ('rol', 'fecha')
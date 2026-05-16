from django.contrib import admin
from .models import Usuario, Avatar


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'nombre', 'apellido', 'edad', 'peso', 'altura')
    search_fields = ('user__username', 'user__email', 'nombre', 'apellido')
    list_filter = ('edad',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'imagen')
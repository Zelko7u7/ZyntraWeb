from django.contrib import admin
from .models import Rutina, Ejercicio, RutinaEjercicio, Entrenamiento


@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'objetivo', 'nivel', 'duracion_min')
    search_fields = ('nombre', 'objetivo')


@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'grupo_muscular', 'tipo')
    search_fields = ('nombre', 'grupo_muscular')


@admin.register(RutinaEjercicio)
class RutinaEjercicioAdmin(admin.ModelAdmin):
    list_display = ('rutina', 'ejercicio', 'orden', 'series', 'repeticiones')


@admin.register(Entrenamiento)
class EntrenamientoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rutina', 'fecha', 'duracion', 'calorias', 'estado')
    list_filter = ('estado', 'fecha')
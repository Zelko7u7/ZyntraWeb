from django.contrib import admin
from .models import Nivel, Rango, Progreso


@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
    list_display = ('numero', 'xp_requerida')


@admin.register(Rango)
class RangoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'xp_min', 'xp_max')


@admin.register(Progreso)
class ProgresoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nivel', 'rango', 'xp_total', 'racha_actual', 'mejor_racha')
    list_filter = ('nivel', 'rango')
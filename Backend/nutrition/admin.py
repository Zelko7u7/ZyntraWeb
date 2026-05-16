from django.contrib import admin
from .models import PlanNutricional, RegistroComida


@admin.register(PlanNutricional)
class PlanNutricionalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'calorias', 'proteinas', 'carbs', 'grasas')


@admin.register(RegistroComida)
class RegistroComidaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'plan', 'fecha', 'calorias')
    list_filter = ('fecha',)
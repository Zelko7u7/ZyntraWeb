from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Entrenamiento
from progress.models import Progreso, Nivel, Rango


@receiver(pre_save, sender=Entrenamiento)
def guardar_estado_anterior(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._estado_anterior = Entrenamiento.objects.get(pk=instance.pk).estado
        except Entrenamiento.DoesNotExist:
            instance._estado_anterior = None
    else:
        instance._estado_anterior = None


@receiver(post_save, sender=Entrenamiento)
def actualizar_progreso(sender, instance, created, **kwargs):
    estado_anterior = getattr(instance, '_estado_anterior', None)

    # Solo procesar cuando el entrenamiento pasa a "completado" por primera vez
    recien_completado = (
        (created and instance.estado == "completado") or
        (not created and instance.estado == "completado" and estado_anterior != "completado")
    )
    if not recien_completado:
        return

    try:
        progreso = Progreso.objects.get(usuario=instance.usuario)
    except Progreso.DoesNotExist:
        return

    # XP basada en duración del entrenamiento
    xp_ganada = 50 + instance.duracion

    progreso.xp_total += xp_ganada
    progreso.calorias_totales += int(instance.calorias)
    progreso.entrenamientos += 1

    # Racha: verificar si hubo entrenamiento completado ayer
    ayer = timezone.now().date() - timezone.timedelta(days=1)
    hubo_entrenamiento_ayer = Entrenamiento.objects.filter(
        usuario=instance.usuario,
        fecha__date=ayer,
        estado="completado"
    ).exclude(pk=instance.pk).exists()

    if hubo_entrenamiento_ayer:
        progreso.racha_actual += 1
    else:
        progreso.racha_actual = 1

    if progreso.racha_actual > progreso.mejor_racha:
        progreso.mejor_racha = progreso.racha_actual

    # Nivel: el más alto cuya xp_requerida no supere el xp_total
    nuevo_nivel = Nivel.objects.filter(
        xp_requerida__lte=progreso.xp_total
    ).order_by('-xp_requerida').first()
    if nuevo_nivel:
        progreso.nivel = nuevo_nivel

    # Rango: el que contenga el xp_total actual
    nuevo_rango = Rango.objects.filter(
        xp_min__lte=progreso.xp_total,
        xp_max__gte=progreso.xp_total
    ).first()
    if nuevo_rango:
        progreso.rango = nuevo_rango

    progreso.save()

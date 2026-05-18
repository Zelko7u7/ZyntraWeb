from django.db.models import F
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from progress.models import Nivel, Progreso, Rango
from .models import Logro, LogroUsuario


def _recompute_nivel_rango(perfil):
    progreso = Progreso.objects.filter(usuario=perfil).first()
    if not progreso:
        return

    progreso.refresh_from_db(fields=["xp_total"])
    xp = progreso.xp_total

    nivel = (
        Nivel.objects
        .filter(xp_requerida__lte=xp)
        .order_by("-xp_requerida")
        .first()
    )
    rango = Rango.objects.filter(xp_min__lte=xp, xp_max__gte=xp).first()

    fields = []
    if nivel and progreso.nivel_id != nivel.id:
        progreso.nivel = nivel
        fields.append("nivel")
    if rango and progreso.rango_id != rango.id:
        progreso.rango = rango
        fields.append("rango")
    if fields:
        progreso.save(update_fields=fields)


def _aplicar_delta_xp(perfil, delta):
    if delta == 0 or perfil is None:
        return
    Progreso.objects.filter(usuario=perfil).update(
        xp_total=F("xp_total") + delta
    )
    _recompute_nivel_rango(perfil)


@receiver(post_save, sender=LogroUsuario)
def sumar_xp_al_desbloquear(sender, instance, created, **kwargs):
    if not created:
        return
    _aplicar_delta_xp(instance.usuario, instance.logro.xp)


@receiver(post_delete, sender=LogroUsuario)
def restar_xp_al_bloquear(sender, instance, **kwargs):
    try:
        xp = instance.logro.xp
    except Logro.DoesNotExist:
        return
    _aplicar_delta_xp(instance.usuario, -xp)


@receiver(pre_save, sender=Logro)
def ajustar_xp_al_editar_logro(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        anterior = Logro.objects.get(pk=instance.pk)
    except Logro.DoesNotExist:
        return

    delta = instance.xp - anterior.xp
    if delta == 0:
        return

    for lu in LogroUsuario.objects.filter(logro=instance).select_related("usuario"):
        _aplicar_delta_xp(lu.usuario, delta)

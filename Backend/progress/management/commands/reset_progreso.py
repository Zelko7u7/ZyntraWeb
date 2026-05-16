from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from progress.models import Progreso, Nivel, Rango


class Command(BaseCommand):
    help = 'Resetea el progreso de un usuario por username. XP, racha y contadores a 0.'

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            type=str,
            help='Username de Django del usuario a resetear.'
        )

    def handle(self, *args, **options):
        username = options['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'No existe el usuario "{username}".')

        try:
            progreso = Progreso.objects.get(usuario__user=user)
        except Progreso.DoesNotExist:
            raise CommandError(f'El usuario "{username}" no tiene Progreso asociado.')

        nivel_base = Nivel.objects.order_by('xp_requerida').first()
        rango_base = Rango.objects.order_by('xp_min').first()

        progreso.xp_total = 0
        progreso.racha_actual = 0
        progreso.mejor_racha = 0
        progreso.calorias_totales = 0
        progreso.entrenamientos = 0
        progreso.nivel = nivel_base
        progreso.rango = rango_base
        progreso.save()

        self.stdout.write(self.style.SUCCESS(
            f'✓ Progreso de "{username}" reseteado a 0.'
        ))

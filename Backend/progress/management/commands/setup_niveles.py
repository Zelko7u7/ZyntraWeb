from django.core.management.base import BaseCommand
from progress.models import Nivel, Rango


class Command(BaseCommand):
    help = 'Crea/actualiza la tabla Nivel con incrementos de 2000 XP y los rangos por defecto.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--max-nivel',
            type=int,
            default=50,
            help='Cantidad de niveles a generar (por defecto 50).'
        )
        parser.add_argument(
            '--xp-por-nivel',
            type=int,
            default=2000,
            help='XP necesaria por nivel (por defecto 2000).'
        )

    def handle(self, *args, **options):
        max_nivel = options['max_nivel']
        xp_step = options['xp_por_nivel']

        Nivel.objects.all().delete()
        for numero in range(1, max_nivel + 1):
            xp_requerida = (numero - 1) * xp_step
            Nivel.objects.create(numero=numero, xp_requerida=xp_requerida)
        self.stdout.write(self.style.SUCCESS(
            f'✓ Creados {max_nivel} niveles, cada uno separado por {xp_step} XP.'
        ))

        rangos_default = [
            ('Principiante', 0, 9999),
            ('Intermedio', 10000, 29999),
            ('Avanzado', 30000, 59999),
            ('Elite', 60000, 99999),
            ('Legendario', 100000, 999999),
        ]

        Rango.objects.all().delete()
        for nombre, xp_min, xp_max in rangos_default:
            Rango.objects.create(nombre=nombre, xp_min=xp_min, xp_max=xp_max)
        self.stdout.write(self.style.SUCCESS(
            f'✓ Creados {len(rangos_default)} rangos.'
        ))

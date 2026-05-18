from django.core.management.base import BaseCommand
from django.core.management import call_command
from progress.models import Nivel
from achievements.models import Logro


class Command(BaseCommand):
    help = (
        "Siembra idempotente. Crea niveles/rangos solo si la tabla Nivel está "
        "vacía y el logro global 'Iniciar cuenta' si aún no existe. "
        "Pensado para ejecutarse al arranque del contenedor."
    )

    def handle(self, *args, **options):
        if Nivel.objects.exists():
            self.stdout.write(self.style.WARNING(
                f"Nivel ya tiene {Nivel.objects.count()} registros, "
                "no se siembra de nuevo."
            ))
        else:
            self.stdout.write("Sembrando niveles y rangos iniciales...")
            call_command("setup_niveles")

        logro_inicio_existe = Logro.objects.filter(
            nombre="Iniciar cuenta",
            usuario__isnull=True,
        ).exists()
        if not logro_inicio_existe:
            Logro.objects.create(
                nombre="Iniciar cuenta",
                xp=50,
                usuario=None,
            )
            self.stdout.write(self.style.SUCCESS(
                "✓ Logro global 'Iniciar cuenta' creado."
            ))
        else:
            self.stdout.write(self.style.WARNING(
                "Logro global 'Iniciar cuenta' ya existe, se omite."
            ))

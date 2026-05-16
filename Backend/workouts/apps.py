from django.apps import AppConfig


class WorkoutsConfig(AppConfig):
    name = 'workouts'

    def ready(self):
        import workouts.signals  # noqa: F401

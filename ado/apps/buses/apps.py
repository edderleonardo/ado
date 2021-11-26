from django.apps import AppConfig


class BusesConfig(AppConfig):
    name = 'ado.apps.buses'
    verbose_name = "Buses"

    def ready(self) -> None:
        try:
            import ado.apps.buses.signals
        except ImportError:
            pass

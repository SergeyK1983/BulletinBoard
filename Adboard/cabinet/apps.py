from django.apps import AppConfig


class CabinetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cabinet'

    def ready(self):
        # Чтобы работали сигналы в signal.py нужно переопределить этот метод
        import cabinet.signals


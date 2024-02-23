from django.apps import AppConfig


class ComentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coment'

    def ready(self):
        # Чтобы работали сигналы в signal.py нужно переопределить этот метод
        import coment.signals

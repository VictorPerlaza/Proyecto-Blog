from django.apps import AppConfig


class BlgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blg'

# blog/apps.py

# apps.py o al final de models.py
from django.apps import AppConfig

class BlogConfig(AppConfig):
    name = 'tu_app_blog'

    def ready(self):
        import blg.signals  # Asegúrate de tener importada la señal

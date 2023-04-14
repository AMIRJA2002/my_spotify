from django.apps import AppConfig


class MusicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spotify_app.music'

    def ready(self):
        from . import signals

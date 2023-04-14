from django.apps import AppConfig


class PlaylistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spotify_app.playlist'

    def ready(self):
        import spotify_app.playlist.signals

from django.db.models.signals import post_save
from .services import set_music_duration
from spotify_app.music.models import Music
from django.dispatch import receiver


@receiver(post_save, sender=Music)
def get_music_duration(sender, instance, **kwargs):
    set_music_duration(instance)
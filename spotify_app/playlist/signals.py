from django.db.models.signals import post_save
from django.dispatch import receiver
from spotify_app.users.models import BaseUser
from .services import create_new_playlist


@receiver(post_save, sender=BaseUser)
def create_like_song_playlist(sender, instance, **kwargs):
    print(instance)
    create_new_playlist(user=instance)



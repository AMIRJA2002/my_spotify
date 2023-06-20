from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from spotify_app.users.models import ArtistProfile


User = get_user_model()


def check_for_existing_user(value: str):
    if User.objects.filter(email=value).exists():
        return True
    return False


def get_user(email):
    return User.objects.get(email=email)


def get_all_artists():
    return User.objects.filter(roll=0)

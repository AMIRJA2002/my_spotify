from .models import PlayList
from django.shortcuts import get_object_or_404



def get_playlist(user, playlist_id=None):
    if not playlist_id:
        playlist = PlayList.objects.filter(user=user)
    else:
        playlist = PlayList.objects.filter(user=user, id=playlist_id)
    return playlist


def get_single_playlist(id, user):
    return get_object_or_404(PlayList, id=id, user=user)

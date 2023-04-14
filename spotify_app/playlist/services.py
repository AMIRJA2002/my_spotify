from django.shortcuts import get_object_or_404

from .models import PlayList
from rest_framework import status
from rest_framework.response import Response


def create_new_playlist(user):
    playlists_count = PlayList.objects.filter(user=user).count()

    if playlists_count > 0:
        name = f"Play List #{playlists_count+1}"
        return PlayList.objects.create(user=user, name=name)
    else:
        return PlayList.objects.create(user=user, name='Liked Songs')


def update_playlist(data, playlist):
    name = data.get('name', playlist.name)
    image = data.get('image', playlist.image)
    description = data.get('description', playlist.description)

    playlist.name = name
    playlist.image = image
    playlist.description = description
    playlist.save()

    return playlist


def delete_playlist(user, playlist_id):
    play_list = get_object_or_404(PlayList, id=playlist_id, user=user)

    if play_list.user == user:
        play_list.delete()
    else:
        pass
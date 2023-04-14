from .models import PlayList


def get_playlist(user, playlist_id):
    playlist = PlayList.objects.get(id=playlist_id, user=user)
    return playlist

from .models import PlayList, AddSongAndDateAdded
from spotify_app.music.models import MusicUpload
from django.shortcuts import get_object_or_404


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


def add_to_playlist(data):
    playlist_id = data.get('playlist')
    song_id = data.get('song')
    playlist = PlayList.objects.get(id=playlist_id)
    song = MusicUpload.objects.get(id=song_id)

    try:
        new_playlist_song = AddSongAndDateAdded.objects.create(song=song, playlist=playlist)
    except:
        return False

    playlist.song_number += 1
    if playlist.duration is None:
        playlist.duration = song.duration
    else:
        playlist.duration += song.duration
    playlist.save()

    return new_playlist_song


def remove_to_playlist(data):
    playlist_id = data.get('playlist')
    song_id = data.get('song')
    playlist = PlayList.objects.get(id=playlist_id)
    song = MusicUpload.objects.get(id=song_id)

    try:
        AddSongAndDateAdded.objects.get(song=song, playlist=playlist).delete()
    except:
        return False

    playlist.song_number -= 1
    playlist.save()

    return True

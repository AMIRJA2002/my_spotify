from .models import Album, MusicUpload
from datetime import timedelta
import mutagen


def create_album(data, user):
    release_date = data.get('release_date')
    cover = data.get('cover')
    new_album = Album.objects.create(
        singer=user,
        cover=cover,
        release_date=release_date,
    )
    return new_album


def add_music(data, request):
    albums = data.get('album')
    cover = data.get('cover')
    name = data.get('name')
    release_data = data.get('release_data')
    song = data.get('song')

    new_music = MusicUpload.objects.create(
        singer=request.user,
        cover=cover,
        name=name,
        release_data=release_data,
        song=song,
    )
    new_music.album.set(albums)
    duration = set_music_duration(new_music)
    new_music.duration = duration
    incrace_album_song_number(albums)
    new_music.save()
    return new_music


def incrace_album_song_number(albums):
    album_ids = [album.id for album in albums]
    albums = Album.objects.filter(id__in=album_ids)

    for album in albums:
        album.songs_number += 1
        album.save()


def set_music_duration(music_instance):
    file_path = music_instance.song.path
    music = mutagen.File(file_path)
    duration = music.info.length
    minutes, seconds = divmod(duration, 60)
    duration = timedelta(minutes=minutes, seconds=seconds)
    return duration

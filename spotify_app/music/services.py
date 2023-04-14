from .models import Album, Music
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


def add_music(data):
    singer = data.get('singer')
    album = data.get('album')
    cover = data.get('cover')
    name = data.get('name')
    release_date = data.get('release_date')
    music = data.get('music')

    new_music = Music.objects.create(
        singer=singer,
        album=album,
        cover=cover,
        name=name,
        release_date=release_date,
        music=music
    )
    return new_music


def set_music_duration(music_instance):
    file_path = music_instance.music.path
    music = mutagen.File(file_path)
    duration = music.info.length
    minutes, seconds = divmod(duration, 60)
    print(duration, 400 * '*')
    music_instance.minutes = timedelta(minutes=minutes, seconds=seconds)

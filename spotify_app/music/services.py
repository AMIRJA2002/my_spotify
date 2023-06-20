from django.shortcuts import get_object_or_404

from .models import Album, MusicUpload, SingerProfile, TopTenSongForArtist
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


def create_artist_profile(request, data):
    artist_profile = SingerProfile.objects.create(
        singer=request.user, name=data.validated_data['name'], image=data.validated_data['image']
    )
    return artist_profile


def create_top_ten_list(request, data):
    return TopTenSongForArtist.objects.create(profile=request.user.singer_profile, music=data.validated_data['music'])


def delete_music_from_top_ten(request, id):
    music = get_object_or_404(TopTenSongForArtist, profile__singer=request.user, id=id)
    music.delete()
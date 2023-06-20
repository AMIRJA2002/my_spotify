from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from spotify_app.music.models import MusicUpload, SingerProfile, TopTenSongForArtist
from .models import Album

User = get_user_model()

def return_all_musics_or_specific_number_number(numbers):
    if numbers is None:
        musics = MusicUpload.objects.all()
        return musics
    elif numbers is not None:
        numbers = int(numbers)
        musics = MusicUpload.objects.filter(genre=numbers)
        return musics


def get_albums(album_id=None):
    if album_id is None:
        albums = Album.objects.all()
        return albums
    elif album_id:
        albums = Album.objects.filter(id=id)
        return albums


def get_artist_albums(user):
    return Album.objects.filter(singer=user)


def get_artist(artist_id):
    return get_object_or_404(SingerProfile, id=artist_id)


def get_top_ten_list(artist_id):
    user = User.objects.get(id=artist_id)
    return TopTenSongForArtist.objects.filter(profile__singer=user)


def get_top_ten(request):
    user = request.user
    return get_object_or_404(TopTenSongForArtist, profile__singer=user)

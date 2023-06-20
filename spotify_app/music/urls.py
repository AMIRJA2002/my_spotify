from django.urls import path
from . import apis


urlpatterns = [
    path('create-album/', apis.AddAlbum.as_view(), name='add-album'),
    path('add-music/', apis.UploadSongAndAddToAlbum.as_view(), name='add-music'),
    path('user-music/', apis.UploadSongAndAddToAlbum.as_view(), name='add-music'),
    path('all-musics/', apis.ReturnAllMusic.as_view(), name='add-music'),
    path('albums/', apis.Albums.as_view(), name='albums'),
    path('artist-albums/', apis.ArtistAlbum.as_view(), name='albums'),
    path('artist-profile/', apis.ArtistProfileView.as_view(), name='artist_profile'),
    path('top-ten/', apis.CreateTopTenView.as_view(), name='top-ten-music'),
]

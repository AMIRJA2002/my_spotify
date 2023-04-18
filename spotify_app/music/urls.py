from django.urls import path
from . import apis


urlpatterns = [
    path('create-album/', apis.AddAlbum.as_view(), name='add-album'),
    path('add-music/', apis.UploadSongAndAddToAlbum.as_view(), name='add-music'),
]

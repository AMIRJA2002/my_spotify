from django.urls import path
from . import apis


urlpatterns = [
    path('create-album/', apis.AddAlbum.as_view(), name='add-album'),
    path('add-music/', apis.AddMusic.as_view(), name='add-music'),
]

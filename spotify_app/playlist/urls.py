from django.urls import path
from . import apis


urlpatterns = [
    path('create/', apis.CreatePlayListApi.as_view(), name='create-playlist'),
    path('update/<int:playlist_id>/', apis.UpdatePlayListApi.as_view(), name='update-playlist'),
    path('delete/<int:playlist_id>/', apis.DeletePlaylistApi.as_view(), name='delete-playlist'),
]

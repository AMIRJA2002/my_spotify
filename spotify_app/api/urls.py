from django.urls import path, include

urlpatterns = [
    path('users/', include('spotify_app.users.urls')),
    path('playlist/', include('spotify_app.playlist.urls')),
    path('music/', include('spotify_app.music.urls')),
]

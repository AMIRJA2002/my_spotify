from django.contrib import admin
from .models import Album, Music


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('singer', 'release_date', 'songs_number', 'like_count')


@admin.register(Music)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('singer', 'release_date', 'like_count')

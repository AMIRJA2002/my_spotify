from django.contrib import admin
from .models import Album, MusicUpload


class SongInline(admin.TabularInline):
    model = Album.musics.through


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('singer', 'release_date', 'songs_number', 'like_count')
    inlines = (SongInline,)


# @admin.register(Music)
# class AlbumAdmin(admin.ModelAdmin):
#     list_display = ('singer', 'release_date', 'like_count')

@admin.register(MusicUpload)
class MusicUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'release_data', 'play_count', 'duration')

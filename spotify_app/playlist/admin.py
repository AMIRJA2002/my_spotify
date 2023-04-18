from .models import PlayList, AddSongAndDateAdded
from django.contrib import admin


class SongDateAddedTOPlaylistAdmin(admin.TabularInline):
    model = AddSongAndDateAdded


@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    inlines = (SongDateAddedTOPlaylistAdmin,)


@admin.register(AddSongAndDateAdded)
class SongDateAddedTOPlaylistAdmin(admin.ModelAdmin):
    list_display = ('playlist', 'date_added')

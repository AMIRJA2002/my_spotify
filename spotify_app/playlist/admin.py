from django.contrib import admin
from .models import PlayList


@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')

from spotify_app.music.models import MusicUpload
from spotify_app.common.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PlayList(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='play_lists')
    description = models.TextField(max_length=1000, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    song_number = models.IntegerField(default=0)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.user}, {self.name}'


class AddSongAndDateAdded(models.Model):
    song = models.OneToOneField(MusicUpload, related_name='songs', on_delete=models.CASCADE)
    playlist = models.ForeignKey(PlayList, related_name='date_added', on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.date_added)}"



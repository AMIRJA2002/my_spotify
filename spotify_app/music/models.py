from django.db import models
from spotify_app.common.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Album(BaseModel):
    singer = models.ForeignKey(User, related_name='Albums', on_delete=models.DO_NOTHING)
    release_date = models.DateField(auto_now_add=False)
    songs_number = models.IntegerField(default=0)
    cover = models.ImageField(upload_to='album/', blank=True, null=True)
    like_count = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.singer)


class MusicUpload(BaseModel):
    singer = models.ForeignKey(User, related_name='user_songs', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='musics/cover/')
    release_data = models.DateField(auto_now_add=False)
    play_count = models.BigIntegerField(default=0)
    duration = models.DurationField(null=True, blank=True)
    song = models.FileField(upload_to='musics/')
    like_count = models.BigIntegerField(default=0)
    album = models.ManyToManyField(Album, related_name='musics')


class SongFit(models.Model):
    song = models.ForeignKey(MusicUpload, related_name='song_feats', on_delete=models.CASCADE)
    singer = models.ForeignKey(User, related_name='song_feats', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.song.name} fit {str(self.singer)}'

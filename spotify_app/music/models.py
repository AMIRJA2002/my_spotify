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


class Music(BaseModel):
    singer = models.ForeignKey(User, related_name='Musics', on_delete=models.DO_NOTHING)
    album = models.ForeignKey(Album, related_name='Musics', on_delete=models.DO_NOTHING, blank=True, null=True)
    cover = models.ImageField(upload_to='musics/cover/', blank=True, null=True)
    name = models.CharField(max_length=333)
    release_date = models.DateField(auto_now_add=False)
    number_heard = models.BigIntegerField(default=0)
    minutes = models.DurationField(null=True, blank=True)
    music = models.FileField(upload_to='musics/')
    like_count = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.name}, f{self.singer}"

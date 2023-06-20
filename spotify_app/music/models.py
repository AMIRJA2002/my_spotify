from django.db import models
from spotify_app.common.models import BaseModel
from django.contrib.auth import get_user_model
from spotify_app.users.models import BaseUser, ArtistProfile

# User = get_user_model()
User = BaseUser


class Album(BaseModel):
    name = models.CharField(max_length=200)
    singer = models.ForeignKey(User, related_name='Albums', on_delete=models.DO_NOTHING)
    release_date = models.DateField(auto_now_add=False)
    songs_number = models.IntegerField(default=0)
    cover = models.ImageField(upload_to='album/', blank=True, null=True)
    like_count = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.singer)


class MusicUpload(BaseModel):
    POP = 0
    CLASSIC = 1
    BLUES = 2
    HIP_HOP = 3
    ROCK = 4
    METAL = 5
    music_genre = (
        (POP, 'پاپ'),
        (CLASSIC, 'کلاسیک'),
        (BLUES, 'بلوز'),
        (HIP_HOP, 'هیپ هاپ'),
        (ROCK, 'راک'),
        (METAL, 'متال'),
    )

    HAPPY = 0
    SAD = 1
    music_type = (
        (HAPPY, 'شاد'),
        (SAD, 'غمگین'),
    )

    genre = models.SmallIntegerField(choices=music_genre, default=POP)
    happy_or_sad = models.SmallIntegerField(choices=music_type, default=SAD)
    singer = models.ForeignKey(User, related_name='user_songs', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='musics/cover/')
    release_data = models.DateField(auto_now_add=False)
    play_count = models.BigIntegerField(default=0)
    duration = models.DurationField(null=True, blank=True)
    song = models.FileField(upload_to='musics/')
    album = models.ManyToManyField(Album, related_name='musics')


class SongFit(models.Model):
    song = models.ForeignKey(MusicUpload, related_name='song_feats', on_delete=models.CASCADE)
    singer = models.ForeignKey(User, related_name='song_feats', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.song.name} fit {str(self.singer)}'


class SingerProfile(models.Model):
    singer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='singer_profile')
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='singer/image/')

    def __str__(self):
        return f'{self.name}'


class TopTenSongForArtist(models.Model):
    music = models.ForeignKey(MusicUpload, on_delete=models.CASCADE, related_name='top_tens')
    profile = models.ForeignKey(SingerProfile, on_delete=models.CASCADE, related_name='top_tens')

    def __str__(self):
        return f'{self.music.name}. {self.profile.name}'

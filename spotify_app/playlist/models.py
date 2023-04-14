from django.db import models
from spotify_app.common.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


class PlayList(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='play_lists')
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    song_number = models.IntegerField(default=0)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.user}, {self.name}'

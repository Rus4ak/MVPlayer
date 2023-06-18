from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from datetime import datetime

# Create your models here.
class Genre(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='img/profile/', default='img/profile/icon_user_default.png')


class Song(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Название'))
    icon = models.ImageField(upload_to='img/', verbose_name=_('Иконка'))
    audio_file = models.FileField(
        upload_to='music/',
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])],
        verbose_name=_('Аудио файл')
    )
    date = models.DateTimeField(default=datetime.now, blank=True)
    genre = models.ManyToManyField(Genre, verbose_name=_('Жанр'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='like_song')

    def __str__(self) -> str:
        return self.title
    
    def likes_count(self):
        return self.like.count()


class Playlist(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Название'))
    song = models.ManyToManyField(Song, verbose_name=_('Музыка'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)

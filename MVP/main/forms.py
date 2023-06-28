from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Song, Playlist, Genre

class AudioFileForm(forms.ModelForm):
    title = forms.CharField(label=_('Название'))
    icon = forms.ImageField(label=_('Иконка'))
    audio_file = forms.FileField(label=_('Аудио файл'))
    genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        label=_('Жанр'),
        widget=forms.SelectMultiple
    )

    class Meta:
        model = Song
        fields = ('title', 'icon', 'audio_file', 'genre')
        exclude = ('user',)


class PlaylistFileForm(forms.ModelForm):
    title = forms.CharField(label=_('Название'))
    song = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(),
        label=_('Музыка'),
        widget=forms.SelectMultiple
    )

    class Meta:
        model = Playlist
        fields = ('title', 'song')
        exclude = ('user',)

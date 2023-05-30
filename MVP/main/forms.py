from django import forms
from .models import Song, Playlist

class AudioFileForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('title', 'icon', 'audio_file', 'genre')
        exclude = ('user',)


class PlaylistFileForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('title', 'song')
        exclude = ('user',)

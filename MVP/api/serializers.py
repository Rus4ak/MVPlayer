from django.contrib.auth.models import User
from rest_framework import serializers
from main.models import Song

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'genre', 'like', 'date', 'user', 'icon', 'audio_file')
        model = Song


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username', 'email')
        model = User

from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import SongSerializer, UserSerializer
from .permissions import IsAuthorOrReadOnly
from main.models import Song


class SongList(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly, )
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthorOrReadOnly, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

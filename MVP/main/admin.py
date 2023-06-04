from django.contrib import admin
from .models import (
    Song,
    Genre,
    Profile,
    Playlist
)

# Register your models here.

admin.site.register((
    Song,
    Genre,
    Profile,
    Playlist
))

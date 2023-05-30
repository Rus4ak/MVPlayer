from django.core.cache import cache
from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Song, Profile, Playlist

# Clear cache if new song is added 
@receiver(post_save, sender=Song)
def delete_cache_song(sender, **kwargs):
    cache.clear()


# Clearing cache when deleting a song
@receiver(post_delete, sender=Song)
def delete_cache_delsong(sender, instance, **kwargs):
    cache.clear()


# Clear cache if user likes or unlikes
@receiver(m2m_changed, sender=Song.like.through)
def delete_cache_like(sender, instance, **kwargs):
    cache.clear()


# Clear cache if a song is added to the playlist
@receiver(m2m_changed, sender=Playlist.song.through)
def delete_cache_playlist(sender, instance, **kwargs):
    cache.clear()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

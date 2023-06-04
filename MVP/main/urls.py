from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('best-tracks/', views.best_tracks, name='best_tracks'),
    path('novelties/', views.novelties, name='novelties'),
    path('hits-of-the-week/', views.hits_of_week, name='hits_of_week'),
    path('mix/', views.mix, name='mix'),
    path('best-performers/', views.best_performers, name='best_performers'),
    path('genres/', views.genres, name='genres'),
    path('genres/<str:genre>', views.genre, name='genre'),
    path('add-track/', views.add_track, name='add_track'),
    path('my-track/', views.my_track, name='my_track'),
    path('create-playlist/', views.create_playlist, name='create_playlist'),
    path('playlist/<int:playlist>', views.playlist, name='playlist'),
    path('add-favourite-track/<int:song_id>', views.like, name='like'),
    path('favourite-track', views.favourite_song, name='favourite_song'),
    path('user_songs/<int:user_id>', views.user_songs, name='user'),
    path('delete-song/<int:song_id>', views.delete_song, name='delete_song'),
    path('add-song-playlist/<int:song_id>/<int:playlist_id>', views.add_song_playlist, name='add_song_playlist'),
    path('delete-song-playlist/<int:song_id>/<int:playlist_id>', views.delete_song_playlist, name='delete_song_playlist'),
    path('delete-playlist/<int:playlist_id>', views.delete_playlist, name='delete_playlist'),
    path('edit-playlist/<int:playlist_id>', views.edit_playlist, name='edit_playlist')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

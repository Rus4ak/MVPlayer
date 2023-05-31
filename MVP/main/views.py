from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.cache import never_cache
from django.core.cache import cache
from django.db.models import Count, Subquery, OuterRef

from .models import Song, Genre, Playlist, User, Profile
from .forms import AudioFileForm, PlaylistFileForm
from .utils import handle_uploaded_file

from datetime import date, timedelta
from pathlib import Path
import random
import re

# Create your views here.
def custom_proc(request):
    if request.user.is_authenticated:
    # A context processor that provides 'Playlist.title'
        title = Playlist.objects.values('title', 'id').filter(user=request.user)
        icon_user = Profile.objects.filter(user=request.user).first().icon

        data = {}
        if title:
            data['titles'] = title
        if icon_user:
            data['icon_user'] = icon_user.url

    else:
        data = {
            'not_playlist': None,
            'icon_user': None
        }

    return data


@never_cache
def index(request: HttpRequest) -> HttpResponse:
    response = render(request, 'main/index.html')
    response['Cache-Control'] = 'no-cache', 'no-store', 'must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = 'O'

    return response


def search(request: HttpRequest) -> HttpResponse:
    songs = cache.get('track')
    song_filter = []

    if not songs:
        songs = Song.objects.all()
        cache.set('track', songs, 60 * 60 * 24)
    
    if request.method == 'POST':
        search_post = request.POST.get('search_query')

        for song in songs:
            re_search = re.findall(rf"\b.*{search_post.lower()}.*\b", song.title.lower()) 

            if re_search:
                song_filter.append(song)

    context = {
        'song': song_filter[:5]
    }

    if request.user.is_authenticated:
        liked_songs = Song.objects.filter(like=request.user)
        context['liked_songs'] = liked_songs

    return render(request, 'main/search.html', context)


def add_track(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AudioFileForm(request.POST, request.FILES)
            
            if form.is_valid():
                song = form.save(commit=False)
                song.user = request.user

                audio_file = form.cleaned_data['audio_file']
                compressed_audio_file = handle_uploaded_file(audio_file)
                song.audio_file = compressed_audio_file

                song.save()
                form.save_m2m()
        else:
            form = AudioFileForm()

        context = {
            'form': form,
        }

        return render(request, 'main/add_track.html', context)

    else:
        return render(request, 'main/not_login.html')


def my_track(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        song = cache.get('my_track')

        if not song:
            song = Song.objects.filter(user=request.user)
            cache.set('my_track', song, 60 * 60 * 24)

        context = {
            'song': song,
        }

        liked_songs = Song.objects.filter(like=request.user)
        context['liked_songs'] = liked_songs

        return render(request, 'main/my_track.html', context)

    else:
        return render(request, 'main/not_login.html')


def best_tracks(request: HttpRequest) -> HttpResponse:
    song = cache.get('best_track')

    if not song:
        song = Song.objects.annotate(likes_count=Count('like')).order_by('-likes_count')
        cache.set('best_track', song, 60 * 60 * 24)
 
    context = {
        'song': song[:6],
        'song2': song[6:12],
    }

    if request.user.is_authenticated:
        liked_songs = Song.objects.filter(like=request.user)
        context['liked_songs'] = liked_songs

    return render(request, 'main/bestTracks.html', context)


def novelties(request: HttpRequest) -> HttpResponse:
    song = cache.get('new_track')

    if not song:
        song = Song.objects.all().order_by('-date').select_related('user')[:12]
        cache.set('new_track', song, 60 * 60 * 24)

    context = {
        'song': song[:6],
        'song2': song[6:12],
    }

    if request.user.is_authenticated:
        liked_songs = Song.objects.filter(like=request.user)
        context['liked_songs'] = liked_songs

    return render(request, 'main/novelties.html', context)


def hits_of_week(request: HttpRequest) -> HttpResponse:
    end_week = date.today()
    start_week = end_week - timedelta(days=7)
    
    song = cache.get('hits_of_week')
    
    if not song:
        song = Song.objects.filter(date__date__range=[start_week, end_week]).annotate(likes_count=Count('like')).order_by('-likes_count')
        cache.set('hits_of_week', song, 60 * 60 * 24)

    context = {
        'song': song[:6],
        'song2': song[6:12],
    }

    if request.user.is_authenticated:
        liked_songs = Song.objects.filter(like=request.user)
        context['liked_songs'] = liked_songs

    return render(request, 'main/hits_of_week.html', context)


def mix(request: HttpRequest) -> HttpResponse:
    song = cache.get('shuffled_songs')

    # Shuffle track every 24 hours
    if not song:
        song = list(Song.objects.all().select_related('user')[:12])
        random.shuffle(song)
        cache.set('shuffled_songs', song, 60 * 60 * 24) # Cache on 24 hours
    
    context = {
        'song': song[:6],
        'song2': song[6:12],
    }

    if request.user.is_authenticated:
        liked_songs = Song.objects.filter(like=request.user)
        context['liked_songs'] = liked_songs

    return render(request, 'main/mix.html', context)


def best_performers(request: HttpRequest) -> HttpResponse:
    users = cache.get('best_performers')

    if not users:
        users = Song.objects.values('user').annotate(likes_count=Count('like')).order_by('-likes_count')
        cache.set('best_performers', users, 60 * 60 * 24)
    
    user_ids = [user['user'] for user in users]
    
    users_with_icon = []

    for user_id in user_ids:
        user_name = User.objects.filter(id=user_id).annotate(likes_count=Subquery(users.filter(user=OuterRef('id')).values('likes_count'))).order_by('-likes_count')
        icon = Profile.objects.get(user=user_id)

        user_data = {
            'user_id': user_id,
            'username': user_name[0],
            'icon': icon.icon.url
        }
        
        users_with_icon.append(user_data)
    
    context = {
        'users': users_with_icon[:6],
        'users2': users_with_icon[6:12]
    }

    return render(request, 'main/bestPerformers.html', context)


def genres(request: HttpRequest) -> HttpResponse:
    genre = Genre.objects.all()

    context = {
        'genres': genre[:4],
        'genres2': genre[4:8],
    }

    return render(request, 'main/genres.html', context)


def genre(request: HttpRequest, genre: Genre) -> HttpResponse:
    genre_filter = Genre.objects.get(title=genre)
    song = cache.get(f'genre_track{genre}')

    if not song:
        song = Song.objects.filter(genre=genre_filter.id)
        cache.set(f'genre_track{genre}', song, 60 * 60 * 24)

    context = {
        'genre': genre_filter,
        'song': song[:6],
        'song2': song[6:12]
    }

    if request.user.is_authenticated:
        liked_songs = Song.objects.filter(like=request.user)
        context['liked_songs'] = liked_songs

    return render(request, 'main/genre.html', context)


def create_playlist(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PlaylistFileForm(request.POST, request.FILES)
            
            if form.is_valid():
                playlist = form.save(commit=False)
                playlist.user = request.user
                playlist.save()
                form.save_m2m()
        else:
            form = PlaylistFileForm()

        context = {
            'form': form,
        }

        return render(request, 'main/create_playlist.html', context)

    else:
        return render(request, 'main/not_login.html')
    

def playlist(request: HttpRequest, playlist: Playlist) -> HttpResponse:
    song = cache.get(f'playlist{playlist}')

    if not song:
        playlist_obj = Playlist.objects.select_related('user').prefetch_related('song').get(id=playlist)
        song = playlist_obj.song.all()
        cache.set(f'playlist{playlist}', song, 60 * 60 * 24)

    playlist_title = Playlist.objects.get(id=playlist).title

    context = {
        'playlist_title': playlist_title,
        'playlist_id': playlist,
        'song': song[:6],
        'song2': song[6:12]
    }

    if request.user.is_authenticated:
        liked_songs = Song.objects.filter(like=request.user)
        context['liked_songs'] = liked_songs
    
    return render(request, 'main/playlist.html', context)


def like(request: HttpRequest, song_id: int) -> HttpResponse:
    if request.user.is_authenticated:
        if request.method == 'POST':
            song = cache.get(f'like_track{song_id}')

            if not song:
                song = Song.objects.get(pk=song_id)
                cache.set(f'like_track{song_id}', song, 60 * 60 * 24)

            is_like = False

            if request.user in song.like.all():
                is_like = True

            if not is_like:
                song.like.add(request.user)

            else:
                song.like.remove(request.user)

            random_number = random.randint(1, 1000000)

            response_data = {
                'is_liked': not is_like,
                'random_number': random_number
            }
            return JsonResponse(response_data)


def favourite_song(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        song = cache.get(f'favourite_track{request.user}')

        if not song:
            song = Song.objects.filter(like=request.user)
            cache.set(f'favourite_track{request.user}', song, 60 * 60 * 24)

        context = {
            'song': song[:6],
            'song2': song[6:12]
        }

        return render(request, 'main/favourite_track.html', context)

    else:
        return render(request, 'main/not_login.html')


def user_songs(request: HttpRequest, user_id: User) -> HttpResponse:
    user = User.objects.get(id=user_id)
    song = cache.get(f'user_song{user_id}')

    if not song:
        song = Song.objects.filter(user=user_id)
        cache.set(f'user_song{user_id}', song, 60 * 60 * 24)

    context = {
        'song': song[:6],
        'song2': song[6:12],
        'user': user.username
    }

    if request.user.is_authenticated:
        liked_songs = Song.objects.filter(like=request.user)
        context['liked_songs'] = liked_songs

    return render(request, 'main/user.html', context)


def delete_song(request: HttpRequest, song_id: int) -> HttpResponse:
    song = Song.objects.get(id=song_id)
    song_path = Path(f'{settings.MEDIA_ROOT}\{str(song.audio_file)[6:]}')
    icon_path = Path(f'{settings.MEDIA_ROOT}\{song.icon}')
    
    if request.method == 'POST':
        song_path.unlink()
        icon_path.unlink()
        song.delete()

    return redirect(request.META.get('HTTP_REFERER'))


def add_song_playlist(request: HttpRequest, song_id: int, playlist_id: int) -> HttpResponse:
    if request.method == 'POST':
        song = Song.objects.get(id=song_id)
        playlist = Playlist.objects.get(id=playlist_id)
        
        playlist.song.add(song)

    return redirect(request.META.get('HTTP_REFERER'))


def delete_song_playlist(request: HttpRequest, song_id: int, playlist_id: int) -> HttpResponse:
    if request.method == 'POST':
        song = Song.objects.get(id=song_id)
        playlist = Playlist.objects.get(id=playlist_id)

        playlist.song.remove(song)

    return redirect(request.META.get('HTTP_REFERER'))


def delete_playlist(request:HttpRequest, playlist_id:int) -> HttpResponse:
    if request.method == 'POST':
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.delete()

    return redirect('/')
    
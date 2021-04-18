import logging
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .forms import ViewPlaylistForm
from .models import Playlist, Userbase, Artist, Album
from typing import Dict, List

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

options_to_fields = {
    'artist_name': 'track__artist',
    'album_name': 'track__album',
    'date_added': 'added_at',
    'track_name': 'track__name',
}

@login_required
def index(request):
    context = {}
    resp = render(request, 'user/skeleton.html', context=context)
    return resp

@login_required
def get_tracks_in_playlist(playlist):
    playlist_order = playlist.sort_by
    return playlist.trackplaylists_set.all() \
                .order_by(options_to_fields[playlist_order])

@login_required
def browse(request):
    playlists = Playlist.objects.all()
    curr_user = Userbase.objects.get(username=request.user.username)
    categories: Dict[str, List['QuerySet']] = {}
    categories['Recently Played'] = Playlist.objects.filter(owner__id=curr_user.id) \
                                    .order_by('-last_played_at')
    categories['Top Playlists'] = playlists.order_by('-times_played')[:5]
    categories['Recommended Playlists'] = [
        p for p in playlists if p not in categories['Top Playlists']
    ]
    
    artists = {}
    artists['Featured Artists'] = Artist.objects.all()

    albums = {}
    albums['New Releases'] = Album.objects.all().order_by('-released_at')

    context = {
        'playlist_categories': categories,
        'album_categories': albums,
        'artist_categories': artists,
        'Favourite': curr_user.favourites.all(),
    }

    resp = render(request, 'user/browse.html', context=context)
    resp["X-Frame-Options"] = 'SAMEORIGIN'
    return resp


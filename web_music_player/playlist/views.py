import logging
import json
from datetime import datetime, timezone
from django.db.models import Sum
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ViewPlaylistForm
from user.models import Playlist, Userbase, Track

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@login_required
def update_favourites(request):
    data = json.loads(request.body.decode('utf-8'))
    curr_user = Userbase.objects.get(username=request.user.username)
    now = datetime.now(timezone.utc)
    track = Track.objects.get(id=data['track_id'])
    if request.method == 'POST':
        curr_user.favourites.add(track, through_defaults={'added_at': now})
        info = {'added': True}
    elif request.method == 'DELETE':
        curr_user.favourites.remove(track)
        info = {'removed': True}
    else:
        return 'HTTPNotAllowed'
    return JsonResponse(
        {**{'playlist': curr_user.get_full_name() + "'s Favourites",
            'track': track.title,
            'updated_by': curr_user.username,
            'success': True},
        **info}
    )

# @login_required
def index(request, playlist_id):    
    "changing header is tricky when using generic views"

    curr_user = Userbase.objects.get(username=request.user.username)
    curr_playlist = Playlist.objects.get(id=playlist_id)
    if request.method == 'POST' or request.method == 'DELETE':
        data = json.loads(request.body.decode('utf-8'))
        now = datetime.now(timezone.utc)
        track = Track.objects.get(id=data['track_id'])

        if request.method == 'POST':
            curr_playlist.tracks.add(track, through_defaults={'added_at': now})
            info = {'added': True}
        elif request.method == 'DELETE':    
            curr_playlist.tracks.remove(track)
            info = {'removed': True}
    
        return JsonResponse(
            {**{'playlist': curr_playlist.name,
                'updated_by': curr_user.username,
                'track': track.title,
                'success': True},
            **info}
        )
    elif request.method == 'GET':
        other_playlists = curr_user.playlists.all().order_by('-last_played_at')
        own_playlists = Playlist.objects \
                            .filter(owner__id=curr_user.id) \
                            .order_by('-last_played_at')

        user_playlists = list(own_playlists) + list(other_playlists)
        playlist_duration = curr_playlist.tracks.aggregate(
                     playlist_duration=Sum('duration'))['playlist_duration']
        context = {
            'current_playlist': curr_playlist,
            'playlist_duration': playlist_duration,
            'curr_user': curr_user,
            'playlists': user_playlists,
        }
        resp = render(request, 'user/playlist.html', context=context)
        resp["X-Frame-Options"] = 'SAMEORIGIN'
        return resp
    else:
        return 'HTTPNotAllowed'




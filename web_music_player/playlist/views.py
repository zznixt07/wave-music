import logging
import json
from datetime import datetime, timezone
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ViewPlaylistForm
from user.models import Playlist, Userbase, Track

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# @login_required
def add_to_playlist(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        now = datetime.now(timezone.utc)
        playlist = Playlist.objects.get(id=data['playlist_id'])
        track = Track.objects.get(id=data['track_id'])
        playlist.tracks.add(track, through_defaults={'added_at': now})
    
        response = JsonResponse({
            'playlist': playlist.name,
            'track': track.title,
            'success': True
        })
        return response
    else:
        return 'HTTPNotAllowed'

# @login_required
def index(request):    
    "changing header is tricky when using generic views"

    if request.method == 'GET':
        # user = request.user
        user = Userbase.objects.get(username='zznix')
        other_playlists = user.playlists.all().order_by('-last_played_at')
        own_playlists = Playlist.objects \
                            .filter(owner__id=user.id) \
                            .order_by('-last_played_at')

        playlists = list(own_playlists) + list(other_playlists)
        # form = ViewPlaylistForm()
        context = {
            # 'form': form,
            'playlists': playlists,
        }
        resp = render(request, 'user/playlist.html', context=context)
        resp["X-Frame-Options"] = 'SAMEORIGIN'
    else:
        pass

    return resp


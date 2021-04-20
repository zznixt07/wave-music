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
from user.models import Playlist, Userbase, Track, Album
from playlist.views import get_user_playlists_obj

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def index(request, album_id):
    curr_user = Userbase.objects.get(id=request.user.id)
    curr_album = Album.objects.get(id=album_id)
    if request.method == 'POST' or request.method == 'DELETE':
        data = json.loads(request.body.decode('utf-8'))
        now = datetime.now(timezone.utc)
        track = Track.objects.get(id=data['track_id'])

        if request.method == 'POST':
            curr_album.track_set.add(track, through_defaults={'added_at': now})
            info = {'added': True}
        elif request.method == 'DELETE':    
            curr_album.track_set.remove(track)
            info = {'removed': True}
    
        return JsonResponse({
            **{'playlist': curr_album.name,
                'updated_by': curr_user.username,
                'track': track.title,
                'success': True},
            **info
        })
    elif request.method == 'GET':
        user_playlists = get_user_playlists_obj(request)
        all_artist_albums = {
            "More From " + ', '.join([c.get_full_name() for c in curr_album.artist.all()]): 
                Album.objects.filter(id=album_id)
        }
        album_duration = curr_album.track_set.aggregate(
            album_duration=Sum('duration'))['album_duration']
        context = {
            'current_album': curr_album,
            'album_categories': all_artist_albums,
            'album_duration': album_duration,
            'curr_user': curr_user,
            'playlists': user_playlists,
        }
        resp = render(request, 'album/album.html', context=context)
        resp["X-Frame-Options"] = 'SAMEORIGIN'
        return resp
    else:
        return 'HTTPNotAllowed'

def get_track_ids(request, album_id):
    return JsonResponse([
        t.id for t in Track.objects.filter(album__id=album_id)
    ], safe=False)


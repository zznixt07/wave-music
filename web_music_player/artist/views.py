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
from user.models import Playlist, Userbase, Track, Album, Artist
from playlist.views import get_user_playlists_obj

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@login_required
def index(request, artist_id):
    artist = Artist.objects.get(id=artist_id)
    curr_user_obj = Userbase.objects.get(id=request.user.id)

    if request.method == 'GET':
        is_follower = is_a_follower(request, artist.id, request.user.id)

        tracks = {}
        tracks['Popular'] = Track.objects \
                                .filter(artist__id=artist_id) \
                                .order_by('-total_streams')[:10]
        albums = {}
        # using set, the order is scrambled. althouhg dont really need strict ordering.
        albums['Top Albums'] = set([t.album for t in tracks['Popular']])
        albums['All Albums'] = Album.objects.filter(artist__id=artist_id)
        context = {
            'track_categories': tracks,
            'album_categories': albums,
            'playlists': get_user_playlists_obj(request),
            'user_obj': artist,
            'curr_user_obj': curr_user_obj,
            'is_follower': is_follower,
            'followers': Artist.objects.get(id=artist_id).as_leader.all().count(),
        }
        
        resp = render(request, 'artist/artist.html', context=context)
        resp["X-Frame-Options"] = 'SAMEORIGIN'
        return resp
    else:
        return 'HTTPNotAllowed'

@login_required
def get_track_ids(request, artist_id):
    return JsonResponse([
        t.id for t in Track.objects.filter(artist__id=artist_id)
    ], safe=False)

def is_a_follower(request, leader_id, user_id):
    is_follower = False
    for leader in Userbase.objects.get(id=leader_id).as_leader.all():
        if leader.follower.id == user_id:
            is_follower = True
            break
    return is_follower
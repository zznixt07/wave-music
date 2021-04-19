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

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@login_required
def index(request, artist_id):
    if request.method == 'GET':
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


import os
import logging
import json
from datetime import datetime, timezone
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from user.models import Playlist, Userbase, Track
from django.conf import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

media_root = str(settings.MEDIA_ROOT)
media_set = set(media_root.split(os.path.sep))

# @login_required
def get_track(request, track_id: int):
    if request.method == 'GET':
        track = Track.objects.get(id=track_id)
        slash = os.path.sep
        # img_set = set(track.cover_image.path.split(slash))
        # audio_set = set(track.location.path.split(slash))
        # image_url = slash.join(img_set - media_set)
        # audio_url = slash.join(audio_set - media_set)
        image_url = '/'.join(track.cover_image.path.split(slash)[-2:])
        audio_url = '/'.join(track.location.path.split(slash)[-2:])
        response = JsonResponse({
            'success': True,
            'title': track.title,
            'artists': [
                {a.id: a.get_full_name()} for a in track.artist.all()
            ],
            'album': {track.album.id: track.album.title},
            'genre': track.genre,
            'duration': track.duration,
            'explicit': track.explicit,
            'created_at': track.created_at,
            'total_streams': track.total_streams,
            # 'image_url': track.cover_image.path,
            # 'audio_url': track.location.path,
            'image_url': image_url,
            'audio_url': audio_url,
        }, safe=False)
        return response
    else:
        return 'HTTPNotAllowed'


import logging
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .forms import ViewPlaylistForm
from .models import Playlist, Userbase

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# @login_required
def index(request):
    context = {}
    resp = render(request, 'user/skeleton.html', context=context)
    return resp

# @login_required
def browse(request):
    context = {}
    resp = render(request, 'user/browse.html', context=context)
    resp["X-Frame-Options"] = 'SAMEORIGIN'
    return resp

# @login_required
# def playlist(request):
#     "changing header is tricky when using generic views"

#     if request.method == 'GET':
#         # user = request.user
#         user = Userbase.objects.get(username='zznix')
#         other_playlists = user.playlists.all().order_by('-last_played_at')
#         own_playlists = Playlist.objects \
#                             .filter(owner__id=user.id) \
#                             .order_by('-last_played_at')

#         playlists = list(own_playlists) + list(other_playlists)
#         # form = ViewPlaylistForm()
#         context = {
#             # 'form': form,
#             'playlists': playlists,
#         }
#         resp = render(request, 'user/playlist.html', context=context)
#         resp["X-Frame-Options"] = 'SAMEORIGIN'
#     else:
#         pass

#     return resp


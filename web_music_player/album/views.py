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
from user.models import Playlist, Userbase, Track

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def index(request, artist_id):
    return JsonResponse({})
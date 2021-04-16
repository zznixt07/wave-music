import logging
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
# from .forms import 

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def index(request):
    context = {}
    resp = render(request, 'user/skeleton.html', context=context)
    return resp

def browse(request):
    context = {}
    resp = render(request, 'user/browse.html', context=context)
    resp["X-Frame-Options"] = 'SAMEORIGIN'
    return resp

def playlist(request):
    context = {}
    resp = render(request, 'user/playlist.html', context=context)
    resp["X-Frame-Options"] = 'SAMEORIGIN'
    return resp


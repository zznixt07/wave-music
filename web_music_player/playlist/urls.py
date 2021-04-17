from django.urls import path, include
from . import views

app_name = 'site_playlist'
urlpatterns = [
    path('', views.index, name='index'),
    path('addToPlaylist/', views.add_to_playlist, name='add_to_playlist'),
]

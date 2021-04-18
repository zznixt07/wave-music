from django.urls import path, include
from . import views

app_name = 'site_playlist'
urlpatterns = [
    path('<int:playlist_id>/', views.index, name='index'),
    # path('addToPlaylist/', views.add_to_playlist, name='add_to_playlist'),
    path('favourites/', views.update_favourites, name='update_favourites'),
]

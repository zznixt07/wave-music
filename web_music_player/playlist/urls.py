from django.urls import path, include
from . import views

app_name = 'site_playlist'
urlpatterns = [
    path('<int:playlist_id>/', views.index, name='index'),
    path('getTracks/<int:playlist_id>/', views.get_track_ids, name='get_track_ids'),
    path('favourites/', views.update_favourites, name='update_favourites'),
]

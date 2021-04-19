from django.urls import path, include
from . import views

app_name = 'site_artist'
urlpatterns = [
    path('<int:artist_id>/', views.index, name='index'),
    path('getTracks/<int:artist_id>/', views.get_track_ids, name='get_track_ids'),
]

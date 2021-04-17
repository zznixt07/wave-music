from django.urls import path, include
from . import views

app_name = 'site_track'
urlpatterns = [
    # path('', views.index, name='index'),
    path('getTrack/<int:track_id>', views.get_track, name='track_details'),
]

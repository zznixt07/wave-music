from django.urls import path, include
from . import views

app_name = 'site_album'
urlpatterns = [
    path('<int:album_id>/', views.index, name='index'),
    path('getTracks/<int:album_id>/', views.get_track_ids, name='get_track_ids'),
]

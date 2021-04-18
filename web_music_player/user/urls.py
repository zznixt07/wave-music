from django.urls import path, include
from . import views

app_name = 'site_user'
urlpatterns = [
    path('', views.index, name='index'),
    path('browse/', views.browse, name='browse'),    
]

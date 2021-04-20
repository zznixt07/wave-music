import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from account.views import OwnPasswordChangeDoneView



urlpatterns = [
    path('', include('user.urls', namespace='user')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('playlist/', include('playlist.urls', namespace='playlist')),
    path('track/', include('track.urls', namespace='track')),
    path('album/', include('album.urls', namespace='album')),
    path('artist/', include('artist.urls', namespace='artist')),
    path('password_change_done/', OwnPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('admin-dashboard/', include('admin.urls')),
]


# ] + [
#     re_path(
#         r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:], 
#         serve,
#         {
#         'document_root': os.path.join(
#             settings.BASE_DIR),
#         'show_indexes' : True})
# ] # remove ..staticfiles from INSTALLED_APPS too.

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
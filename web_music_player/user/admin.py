from django.contrib import admin
from .models import Profile, Userbase, Adminbase, Artist, Album, Track, Playlist, Followers, UserbasePlaylists, FavouritesTracks, TrackPlaylists


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'password',
        'last_login',
        'is_superuser',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
        'description',
        'country',
        'profile_pic',
        'gender',
        'age',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
    )


@admin.register(Userbase)
class UserbaseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'password',
        'last_login',
        'is_superuser',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
        'user_ptr',
        'description',
        'country',
        'profile_pic',
        'gender',
        'age',
        'plan_type',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
        'user_ptr',
    )
    raw_id_fields = ('favourites', 'playlists', 'followers')


@admin.register(Adminbase)
class AdminbaseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'password',
        'last_login',
        'is_superuser',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
        'user_ptr',
        'description',
        'country',
        'profile_pic',
        'gender',
        'age',
        'level',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
        'user_ptr',
    )


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'password',
        'last_login',
        'is_superuser',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
        'user_ptr',
        'description',
        'country',
        'profile_pic',
        'gender',
        'age',
        'profile_ptr',
        'plan_type',
        'social_links',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
        'user_ptr',
        'profile_ptr',
    )


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'released_at',
        'album_type',
        'cover_image',
    )
    list_filter = ('released_at',)
    raw_id_fields = ('artist',)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'genre',
        'released_at',
        'duration',
        'explicit',
        'created_at',
        'total_streams',
        'cover_image',
        'location',
        'album',
    )
    list_filter = ('released_at', 'explicit', 'created_at', 'album')
    raw_id_fields = ('artist',)
    date_hierarchy = 'created_at'


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'privacy_level',
        'sort_by',
        'removable',
        'times_played',
        'last_played_at',
        'last_modified_at',
    )
    list_filter = ('removable', 'last_played_at', 'last_modified_at')
    raw_id_fields = ('owner', 'tracks')
    search_fields = ('name',)


@admin.register(Followers)
class FollowersAdmin(admin.ModelAdmin):
    list_display = ('id', 'leader', 'follower')
    list_filter = ('leader', 'follower')


@admin.register(UserbasePlaylists)
class UserbasePlaylistsAdmin(admin.ModelAdmin):
    list_display = ('id', 'write', 'userbase', 'playlists')
    list_filter = ('write', 'userbase', 'playlists')


@admin.register(FavouritesTracks)
class FavouritesTracksAdmin(admin.ModelAdmin):
    list_display = ('id', 'tracks', 'added_at', 'user')
    list_filter = ('tracks', 'added_at', 'user')


@admin.register(TrackPlaylists)
class TrackPlaylistsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tracks', 'added_at', 'playlists')
    list_filter = ('tracks', 'added_at', 'playlists')

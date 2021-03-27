from django.core.validators import MaxValueValidator
from django.db import models
from datetime import datetime, timezone

GENDER = [
    ('', 'Choose..'),
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
]

HIDE_LEVELS = [
    ('pub', 'public'),
    ('pri', 'private'),
    ('un', 'unlisted')
]

SORT_BY = [
    ('artist', 'artist'),
    ('album', 'album'),
    ('date', 'date added'),
    # TODO: below
    # ('manual', 'custom order')
]

def aware_utc():
    return datetime.now(timezone.utc)


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    privacy_level = models.CharField(max_length=3, choices=HIDE_LEVELS, default='pub',
        verbose_name='restricts other users from viewing this playlist'
        )
    sort_by = models.CharField(max_length=10, choices=SORT_BY, default='date',
        verbose_name='value used to sort the songs inside this playlist.')
    # below filed is not updated when calling .update() on other fields
    # only auto updated when calling .save()
    date_modified = models.DateTimeField(auto_now=True,         
        verbose_name='store the last time when a song was added or removed from this playlist')


class User(models.Model):
    username = models.CharField(max_length=32, unique=True, null=False, blank=False)
    password = models.CharField(max_length=64)
    gender = models.CharField(max_length=20, choices=GENDER, blank=True, default='', null=False)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(150)])
    date_joined = models.DateTimeField('date when the account was created', default=aware_utc)
    playlists = models.ManyToManyField(Playlist)
    # recent_playlist = 
    # recent_songs = 
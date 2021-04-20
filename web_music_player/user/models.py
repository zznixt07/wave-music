import os
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.core.files import File
from datetime import datetime, timezone
# from django.utils import timezone
from PIL import Image
from .constants import *


def aware_utc_now():
    return datetime.now(timezone.utc)


class Profile(User):
    description = models.TextField(max_length=2000, blank=True)
    country = models.CharField(max_length=50, blank=True, choices=COUNTRIES, default='US')
    profile_pic = models.ImageField(upload_to=f'userbase/',  default='userbase/default.jpg')
    gender = models.CharField(max_length=20, choices=GENDER, blank=True, default='', null=False)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(150)], default=None, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        print(repr(self.profile_pic.path))
        with open(self.profile_pic.path, 'rb') as file:
            self.profile_pic.save(
                os.path.basename(self.profile_pic.path),
                File(file),
                save=False,
            )
        super().save(*args, **kwargs)

        # img = Image.open(self.profile_pic.path)
        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     img.save(self.profile_pic.path)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Userbase(Profile):
    plan_type = models.CharField(max_length=10, default='free')
    favourites = models.ManyToManyField('Track', through='FavouritesTracks')
    playlists = models.ManyToManyField('Playlist', through='UserbasePlaylists')
    followers = models.ManyToManyField('self', symmetrical=False, through='Followers',)
    # not symmetrical. If A follows B, then B doesn't neccessarly follow A.

    class Meta:
        verbose_name = 'Userbase'
        verbose_name_plural = 'Userbase'

class Adminbase(Profile):
    level = models.CharField(max_length=1)

    class Meta:
        verbose_name = 'Adminbase'
        verbose_name_plural = 'Adminbase'
    
class Artist(Userbase):
    # secondary_images = models.ImageField(upload_to=f'artist_sec/{self.id}/', blank=True, null=False,default='userbase/default.jpg')
    social_links = models.CharField(max_length=100, null=False, blank=True, default='')

    class Meta:
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'

class Album(models.Model):
    title = models.CharField(max_length=200)
    released_at = models.DateTimeField(null=True)
    album_type = models.CharField('album or single', max_length=10)
    cover_image = models.ImageField(upload_to='album_covers/', default='userbase/default.jpg')
    artist = models.ManyToManyField('Artist')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        with open(self.cover_image.path, 'rb') as file:
            self.cover_image.save(
                os.path.basename(self.cover_image.path),
                File(file),
                save=False,
            )
        super().save(*args, **kwargs)


class Track(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50, choices=GENRES, default='other')
    released_at = models.DateTimeField(null=True)
    duration = models.PositiveIntegerField('duration of track in secs')
    explicit = models.BooleanField()
    created_at = models.DateTimeField('date when the track was uploaded', default=aware_utc_now)
    total_streams = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='track_covers/', default='userbase/default.jpg')
    location = models.FileField(upload_to='track_audio/')
    album = models.ForeignKey('Album', on_delete=models.CASCADE, blank=False, null=True)
    artist = models.ManyToManyField('Artist')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        with open(self.cover_image.path, 'rb') as file:
            self.cover_image.save(
                os.path.basename(self.cover_image.path),
                File(file),
                save=False,
            )
        with open(self.location.path, 'rb') as file:
            self.location.save(
                os.path.basename(self.location.path),
                File(file),
                save=False,
            )
        super().save(*args, **kwargs)


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, blank=True)
    privacy_level = models.CharField(max_length=3, choices=HIDE_LEVELS, default='pub',
        verbose_name='restricts other users from viewing this playlist'
        )

    sort_by = models.CharField(max_length=30, choices=SORT_BY, default='date',
        verbose_name='value used to sort the songs inside this playlist.')
    removable = models.BooleanField(default=True)
    times_played = models.PositiveIntegerField(default=0)
    last_played_at = models.DateTimeField(default=aware_utc_now)
    cover_image = models.ImageField(upload_to='playlist_covers/', default='userbase/default.jpg')
    # below field is not updated when calling .update() on other fields
    # only auto updated when calling .save()
    last_modified_at = models.DateTimeField(auto_now=True,
        verbose_name='store the last time when a track was added or removed from this playlist')
    # cant make owner a OneToOneField because it can be repeated(violates unique constraint)
    owner = models.ManyToManyField('Userbase')
    tracks = models.ManyToManyField('Track', through='TrackPlaylists')

    def __str__(self):
        return self.name + ' by ' + str(self.owner.get().username)


# class PlaylistCategory(models.Model):
#     name = models.CharField(max_length=50, default='', null=False, blank=True)

class Followers(models.Model):
    leader = models.ForeignKey(
        'Userbase',
        on_delete=models.CASCADE,
        related_name='as_leader'
    )
    follower = models.ForeignKey(
        'Userbase',
        on_delete=models.CASCADE,
        related_name='as_follower'
    )

    def __str__(self):
        return f'leader: {self.leader.username} | follower: {self.follower.username}'

    class Meta:
        verbose_name = 'Follower'
        verbose_name_plural = 'Follower'

class UserbasePlaylists(models.Model):
    write = models.BooleanField('whether user can edit playlists or not')
    userbase = models.ForeignKey('Userbase', on_delete=models.CASCADE)
    playlists = models.ForeignKey('Playlist', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.userbase.username} | {self.playlists.name}'

    class Meta:
        verbose_name = 'UserbasePlaylist'
        verbose_name_plural = 'UserbasePlaylists'

class FavouritesTracks(models.Model):
    tracks = models.ForeignKey('Track', on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=aware_utc_now)
    user = models.ForeignKey('Userbase', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'FavouritesTrack'
        verbose_name_plural = 'FavouritesTracks'

class TrackPlaylists(models.Model):
    tracks = models.ForeignKey('Track', on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=aware_utc_now)
    playlists = models.ForeignKey('Playlist', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'TrackPlaylist'
        verbose_name_plural = 'TrackPlaylists'

# class Lyrics(models.Model):
#     content = models.FileField(upload_to='lyrics/')

'''
python manage.py reset_db && python manage.py makemigrations && python manage.py migrate


# ================================== CREATE ==================================
# ================================== CREATE ==================================


from datetime import datetime, timezone
dt = datetime.now(timezone.utc)
from random import randint

def rand_dt():
    return datetime(year=randint(2009, 2021), month=randint(1, 12), day=randint(1, 29), hour=randint(0, 23), minute=randint(0, 59), tzinfo=timezone.utc)


pp = "C:\\Users\\zznixt\\OneDrive\\innit_perhaps\\django_app\\web_app\\web_music_player\\media\\15.jfif"
tp = "C:\\Users\\zznixt\\OneDrive\\innit_perhaps\\django_app\\web_app\\web_music_player\\media\\walking.webm"

media_loc = 'C:\\Users\\zznixt\\OneDrive\\innit_perhaps\\django_app\\web_app\\web_music_player\\media\\'
track_loc = media_loc + 'track_audio - Copy'  + "\\"
album_cov_loc = media_loc + 'album_covers - Copy' + "\\"
track_cov_loc = media_loc + 'track_covers - Copy' + "\\"
user_loc = media_loc + 'userbase - Copy' + "\\"
playlist_loc = media_loc + 'playlist_covers - Copy' + "\\"

pp_list = {'1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.png', 'ab67706f0000000221a2087747d946f16704b8af.jfif', 'ab67706f000000022beb4afd7fe086b75229de46.jfif', 'ab67706f000000023e83e977187d7c77d8d6b9aa.jfif', 'ab67706f0000000245a5db34be4a2f006c08284a.jfif', 'ab67706f0000000250e0321a50e940a674b6444e.jfif', 'ab67706f00000002519fc8771d90f496501a4da3.jfif', 'ab67706f000000027600f8bae4006faffdfc08ce.jfif', 'ab67706f000000028663be06e69f49628cf83a56.jfif', 'ab67706f0000000287972ceeccc8fea92cd21af5.jfif', 'ab67706f0000000291208168c4d7591ce5c87651.jfif', 'ab67706f000000029c0fc8e6c8b620e72661efa9.jfif', 'ab67706f00000002ba77a2166a7b66e9a300ffaa.jfif', 'ab67706f00000002bbf7afae234cf3c684ec7b4f.jfif', 'ab67706f00000002ca64210a23622427ec19c4a6.jfif', 'ab67706f00000002cf8e264c6a92e245402ecb7a.jfif', 'ab67706f00000002cfb9853b43822a01fe707f9a.jfif', 'ab67706f00000002d8c915eea90d28e9bb70f550.jfif', 'ab67706f00000002e6f455f80fe9b1636349ce76.jfif', 'ab67706f000000031be7c010773575779a1feef6.jpg', 'default (1).jfif', 'default (2).jfif', 'default (3).jfif', 'default (4).jfif', 'default.jfif', 'default.jpg', 'PZN_On_Repeat2_DEFAULT-en.jpg', 'PZN_Repeat_Rewind2_DEFAULT-en.jpg', 'time-capsule-blue_DEFAULT-en.jpg'}

def rand_profile_pic():
    return  playlist_loc + pp_list.pop()

# // create user in DB
zznix = Userbase.objects.create_user(first_name='Nisan', last_name='Thapa', gender='male', age=20, profile_pic=rand_profile_pic(), username='zznix', password='1234567890!@#')
shailesh = Userbase.objects.create_user(first_name='Shailesh', last_name='Giri', gender='male', age=22, profile_pic=rand_profile_pic(), username='@10zer', password='1234567890!@#')
kells = Userbase.objects.create_user(first_name='Nischal', last_name='Khatri', gender='male', age=20, profile_pic=rand_profile_pic(), username='kells', password='1234567890!@#')
lekha = Userbase.objects.create_user(first_name='Kamala', last_name='Thapa',gender='female', age=44, profile_pic=rand_profile_pic(), username='lekha', password='brt!@#brt')
galzin = Userbase.objects.create_user(first_name='Phurba Gyalen', last_name='Sherpa',gender='male', age=21, profile_pic=rand_profile_pic(), username='pgal', password='qwertyyuiop!@#')
sunil = Userbase.objects.create_user(first_name='Sunil', last_name='Tamang',gender='male', age=22, profile_pic=rand_profile_pic(), username='tech_tmg', password='qwertyyuiop!@#')
sanjib = Userbase.objects.create_user(first_name='Sanjib', last_name='Limbu',gender='male', age=18, profile_pic=rand_profile_pic(), username='eyes_', password='qwertyyuiop!@#')
raj = Userbase.objects.create_user(first_name='Raj', last_name='Sapkota',gender='male', age=16, profile_pic=rand_profile_pic(), username='sm_hght', password='qwertyyuiop!@#')
pramod = Userbase.objects.create_user(first_name='Pramod', last_name='Timilsina',gender='male', age=50, profile_pic=rand_profile_pic(), username='tm_pramod_t', password='qwertyyuiop!@#')


# // add followers to a user
zznix.followers.add(lekha, kells, shailesh, galzin, sunil, raj)
kells.followers.add(zznix)
shailesh.followers.add(raj)
sunil.followers.add(galzin)
galzin.followers.add(pramod, sunil, shailesh)


# // add artists to DB
pilots = Artist.objects.create_user(first_name='21 Pilots', profile_pic=user_loc+'3.jfif', username='21p', password='kjhKJGU%^$75',)
ryan = Artist.objects.create_user(first_name='Ryan', last_name='Tedder', gender='male', profile_pic=user_loc+'1.jpg', username='rtedder', password='kjhKJGU%^$75',)
one_r = Artist.objects.create_user(first_name='One Republic', profile_pic=user_loc+'13.jfif', username='@1Rp', password='kjhKJGU%^$75',)
tyler = Artist.objects.create_user(first_name='Tyler',gender='male', last_name='lyle', profile_pic=user_loc+'5.jfif', username='tyler_lyle', password='kjhKJGU%^$75',)
andrew = Artist.objects.create_user(first_name='Andrew', gender='male', last_name='Bird', profile_pic=user_loc+'7.jfif', username='bird_andrew', password='kjhKJGU%^$75',)
galantis = Artist.objects.create_user(first_name='Galantis', gender='female', profile_pic=user_loc+'9.jfif', username='@galantis', password='kjhKJGU%^$75',)
midnight = Artist.objects.create_user(first_name='The Midnight', gender='female', profile_pic=user_loc+'12.jfif', username='theMidnight', password='kjhKJGU%^$75',)
wknd = Artist.objects.create_user(first_name='The Weekend', gender='male', profile_pic=user_loc+'11.jfif', username='theweekend', password='kjhKJGU%^$75',)

users = {zznix, shailesh, kells, lekha, galzin, sunil, sanjib, raj, pramod, pilots, ryan, one_r, tyler, andrew, galantis, midnight, wknd,}

# // add followers to artists (same as above-above)
pilots.followers.add(zznix, kells)
one_r.followers.add(zznix)
andrew.followers.add(kells, lekha)
galantis.followers.add(lekha)
midnight.followers.add(kells)

# // create playlist in DB
deez = Playlist.objects.create(name='deezloaderz', description='soundiiz', privacy_level='pub', sort_by='date', cover_image=playlist_loc+'PZN_On_Repeat2_DEFAULT-en.jpg')
catchy = Playlist.objects.create(name='catchy', description='kells playlist', privacy_level='pub', sort_by='date', cover_image=playlist_loc+'time-capsule-blue_DEFAULT-en.jpg')
nword = Playlist.objects.create(name='Nostalgic Songs', description='Songs from 80\'s and 90\'s', cover_image=playlist_loc+'default.jfif')

lst = [
('Life is a Dream - mellow lofi beats to relax to', 'Mellow / jazzy lo-fi hip hop beats to study, relax, sleep, game to. Curated by Birdhouse. IG: @birdhouse.'),
('Most Streamed Songs of the Decade', 'Top streaming songs from each year in the 10s.'),
('US Summer Hits of the 10s', 'Songs from the last decade that will make you sing and dance all summer long!'),
('Discover Weekly', 'Your weekly mixtape of fresh music. Enjoy new music and deep cuts picked for you. Updates every Monday.'),
('Chill Hits', 'Kick back to the best new and recent chill tunes.'),
('Hit Repeat', 'The hits you keep coming back to.'),
('Best of the Decade', '100 popular tracks from the past 10 years.'),
('10s Pop Run', '2010s pop to get those legs moving!'),
('Rock Classics', 'Rock legends and epic songs that continue to inspire generations.'),
('Mega Hit Mix', 'A mega mix of 75 of your favorite songs from the last few years! Cover: Dua Lipa'),
('Top Gaming Tracks', 'The tracks that gamers love.'),
('Positive Vibes', 'Turn that frown upside down with these pop classics.'),
('Disney Hits', 'All your favorite Disney hits. Disney’s Raya and the Last Dragon, in theaters now or order it on Disney+ with Premier Access. Additional fee required.'),
]

for infos in lst:
    pl = Playlist.objects.create(name=infos[0], description=infos[1], cover_image=rand_profile_pic())
    pl.owner.add(users.pop())

# // add a owner to a playlist.
deez.owner.add(zznix)
catchy.owner.add(kells)
nword.owner.add(zznix)

# // add playlists to user library.(Follow playlist)
lekha.playlists.add(deez, through_defaults={'write': True})
kells.playlists.add(deez, through_defaults={'write': False})
zznix.playlists.add(catchy, through_defaults={'write': False})

# // add albums to DB
blur = Album.objects.create(title='BlurryFace', released_at=rand_dt(), album_type='single', cover_image=album_cov_loc+'2.jpg')
ohmymy = Album.objects.create(title='Oh my my', released_at=rand_dt(), album_type='single', cover_image=album_cov_loc+'5.jfif')
fine = Album.objects.create(title='My finest work yet', released_at=rand_dt(), album_type='single', cover_image=album_cov_loc+'7.jfif')
naive = Album.objects.create(title='Naive', released_at=rand_dt(), album_type='album', cover_image=album_cov_loc+'1.jpg')
bone = Album.objects.create(title='Bones', released_at=rand_dt(), album_type='album', cover_image=album_cov_loc+'8.jfif')
general = Album.objects.create(title='Gen', released_at=rand_dt(), album_type='Single', cover_image=album_cov_loc+'4.jpg')

# // add artist(s) to album
blur.artist.add(pilots)
ohmymy.artist.add(one_r)
fine.artist.add(andrew)
naive.artist.add(one_r)
bone.artist.add(one_r, galantis)
general.artist.add(wknd)

# // add tracks to DB (album is optional)
tear = Track.objects.create(title='Tear in my heart', album=blur, genre='rock', released_at=rand_dt(), duration=200, explicit=True, created_at=rand_dt(), total_streams=21, cover_image=track_cov_loc+'5.jfif', location=track_loc+'005-twenty_one_pilots-tear_in_my_heart.mp3')
level = Track.objects.create(title='Level of concern', album=blur, genre='pop', released_at=rand_dt(), duration=170, explicit=False, created_at=rand_dt(), total_streams=21, cover_image=track_cov_loc+'4.jfif', location=track_loc+'smth.mp3')
stressed_out = Track.objects.create(title='Stressed Out', album=blur, genre='rock', released_at=rand_dt(), duration=250, explicit=True, created_at=rand_dt(), total_streams=100, cover_image=track_cov_loc+'2.jpg', location=track_loc+'Guns for hands - Twenty one pilots (Lyrics_) aIJUGZ474HY.m4a')
bones = Track.objects.create(title='Bones', album=bone, genre='pop', released_at=rand_dt(), duration=300, explicit=False, created_at=rand_dt(), total_streams=21, cover_image=track_cov_loc+'1.jpg', location=track_loc+'bones.mp3')
stars = Track.objects.create(title='Counting Stars', album=naive, genre='pop', released_at=rand_dt(), duration=190, explicit=True, created_at=rand_dt(), total_streams=21, cover_image=track_cov_loc+'2.jfif', location=track_loc+'Counting Stars   One Republic.mp3')
smth_i_need = Track.objects.create(title='Something I need', album=naive, genre='pop', released_at=rand_dt(), duration=220, explicit=False, created_at=rand_dt(), total_streams=21, cover_image=track_cov_loc+'7.jfif', location=track_loc+'smth.mp3')
sisyephus = Track.objects.create(title='Sisyephus', album=fine, genre='', released_at=rand_dt(), duration=310, explicit=True, created_at=rand_dt(), total_streams=21, cover_image=track_cov_loc+'3.jfif', location=track_loc+'01 Andrew Bird - Sisyphus.mp3')
switch = Track.objects.create(title='Chemical Switches', album=fine, genre='pop', released_at=rand_dt(), duration=300, explicit=True, created_at=rand_dt(), total_streams=21, cover_image=track_cov_loc+'5.jfif', location=track_loc+'smth.mp3')
starboy = Track.objects.create(title='Starboy', album=general, genre='pop', released_at=rand_dt(), duration=300, explicit=True, created_at=rand_dt(), total_streams=21, cover_image=track_cov_loc+'2.jfif', location=track_loc+'ONEREPUBLIC - Love Runs Out [Hastidownload.com].mp3')


# // add artist(s) to tracks.
tear.artist.add(pilots)
stars.artist.add(one_r)
sisyephus.artist.add(andrew)
bones.artist.add(one_r, galantis)
stressed_out.artist.add(pilots)
smth_i_need.artist.add(one_r)
level.artist.add(pilots)
switch.artist.add(andrew)
starboy.artist.add(wknd)

# // add track(s) to a playlist
deez.tracks.add(tear, stars, sisyephus, bones, stressed_out, smth_i_need, level, switch, starboy, through_defaults={'added_at': dt})
nword.tracks.add(stars, through_defaults={'added_at': dt})
catchy.tracks.add(sisyephus, stars, bones, stressed_out, smth_i_need, level, switch, through_defaults={'added_at': dt})
# adding same tracks overwrites. check before overwrite ??
catchy.tracks.add(sisyephus, stars, through_defaults={'added_at': dt})


# // add track to Favourites
zznix.favourites.add(bones, stressed_out, smth_i_need, level, switch)


# ============================== READ ==============================
# ============================== READ ==============================

# // fetch all albums of an artist (using tracks)
one_r = Artist.objects.get(id=4)
# this below can return duplicate entry. cant do .duplicate() on non-postgres
# hence use python to remove repeated entries
Album.objects.filter(track__artist__id=one_r.id)

# // fetch all albums of an artist (pure process)
one_r = Artist.objects.get(id=4)
Album.objects.filter(artist__id=one_r.id)

# // fetch all tracks in an album
blurry_face = Album.objects.get(id=1)
Track.objects.filter(album__id=blurry_face.id)

# // fetch all tracks in a playlist
deez = Playlist.objects.get(id=1)
deez.tracks.all()

# // fetching users playlists (order by recently played)
zznix = Userbase.objects.get(id=1)
other_playlists = zznix.playlists.all().order_by('-last_played_at')
own_playlists = Playlist.objects.filter(owner__id=zznix.id).order_by('-last_played_at')

# // fetch followers(users) of a playlist
Playlist.objects.get(id=1).userbase_set.all()

# // fetch tracks in a playlists with ordering | Recently played
options_to_fields = {
    'artist_name': 'track__artist',
    'album_name': 'track__album',
    'date_added': 'added_at',
    'track_name': 'track__name',
}
playlist_order = deez.sort_by
deez.trackplaylists_set.all().order_by(options_to_fields[playlist_order])

deez.trackplaylists_set.all().order_by('track__album')
deez.trackplaylists_set.all().order_by('track__artist')
deez.trackplaylists_set.all().order_by('track__name')
deez.trackplaylists_set.all().order_by('added_at')

# // get tracks by genre
Track.objects.filter(genre='pop')

# // get tracks by year
from datetime import datetime, timezone
twenty_twenty = datetime(year=2020, month=1, day=1, tzinfo=timezone.utc)
twenty_twenty_one = datetime(year=2021, month=1, day=1, tzinfo=timezone.utc)
Track.objects.filter(released_at__gte=twenty_twenty, released_at__lte=twenty_twenty_one)

# // get tracks by female artists
Track.objects.filter(artist__gender='female')

# // fetch a user's followers
[e.follower.username for e in Followers.objects.filter(leader=lekha.id)]
[e.follower.username for e in lekha.as_leader.all()]
# []
# means lekha has no followers

# // fetch a user's followings.
[e.leader.username for e in Followers.objects.filter(follower=lekha.id)]
[e.leader.username for e in lekha.as_follower.all()]
# ['zznix']
# means lekha only follows zznix

# // fetch favourites playlist
zznix.favourites.all()
FavouritesTracks.objects.filter(user=zznix.id).order_by('-added_at')

# // fetch album duration
from django.db.models import Sum
blurry_face = Album.objects.get(id=1)
blurry_face.track_set.aggregate(album_duration=Sum('duration'))['album_duration']

# // fetch playlist duration
Playlist.objects.get(id=1).tracks.aggregate(playlist_duration=Sum('duration'))['playlist_duration']


# ================================== UPDATE ==================================
# ================================== UPDATE ==================================


# // update user info
Userbase.objects.filter(id=1).update(
    username='zznixt', password='pass', first_name='Peee', last_name='Poo',
    description='This is my bio', profile_pic='pp', gender='male', age=21)

# // update artist info
Artist.objects.filter(id=1).update(
    username='@twentyonepilots', password='4312' first_name='20+1 ', last_name='pilots',
    description='Level of convern', profile_pic=pp, gender=None, age=32
)

# // update playlist info
Playlist.objects.filter(id=1).update(
    name='deeznuts', description='gottem', privacy_level='pri', followers=1,
    sort_by='track_name', times_played=1, last_played_at=dt, last_modified_at=dt,
)

# // update playlist last modified date (auto_now is only called on .save() no on .update())
Playlist.objects.filter(id=1).update(last_modified_at=datetime.now(timezone.utc))

# // update playlist last played date (trigger before playing a song from a playlist)
Playlist.objects.filter(id=1).update(last_played_at=datetime.now(timezone.utc))

# // increment the times_played (only when pressing big play playlist button)
from django.db.models import F
Playlist.objects.filter(id=1).update(times_played=F('times_played')+1)

# // update album info
Album.objects.filter(id=1).update(
    title='FaceBlurry', genre='pop', explicit=True, cover_image=pp, 
)

# // update track info
Track.objects.filter(id=1).update(
    title='Tear in my <3',  genre='pop', explicit=True, cover_image=pp
)

# // increment count of song streams
Track.objects.filter(id=1).update(total_streams=F('total_streams')+1)


# ============================= DELETE =============================
# ============================= DELETE =============================

# // remove a track
Track.objects.get(id=1).delete()

# // remove a track from a playlist
t1 = Track.objects.get(id=1)
deez.tracks.remove(t1)

# // remove an album
Album.objects.get(id=1).delete()

# // remove an artist (doesnt delete artist's album and tracks from db. only unlinks.)
art = Artist.objects.get(username='@1Rp')
art.delete()
((10, {'app1.Followers': 1, 'app1.Album_artist': 3, 'app1.Track_artist': 3, 'app1.Artist': 1, 'app1.Userbase': 1, 'app1.Profile': 1})

# // remove a user (retrieve user's playlists first and delete playlists manually)
zznix = Userbase.objects.get(id=1)
own_playlists = zznix.playlists.filter(owner__id)
own_playlists.delete()
zznix.delete()

# // remove/unfollow playlist from user library
lekha = Userbase.objects.get(username='lekha')
deez = Playlist.objects.get(id=1)
lekha.playlists.remove(deez)

# // remove playlist
# below all do the same
has_write_permission = kells.userbaseplaylists_set.get(playlists=deez).write
has_write_permission = deez.userbaseplaylists_set.get(userbase=kells).write
has_write_permission = UserbasePlaylists.objects.get(playlists=deez, userbase=kells).write


if has_write_permission:
    deez = Playlist.objects.get(id=1)
    deez.delete()
else:
    print('Cannot delete')

# // unfollow user
zznix = Userbase.objects.get(id=10)
kells = Userbase.objects.get(username='kells')
zznix.followers.remove(kells)

# // unfollow artist
midnight = Artist.objects.get(id=10)
kells = Userbase.objects.get(username='kells')
midnight.followers.remove(kells)

# 

'''

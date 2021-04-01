from django.core.validators import MaxValueValidator
from django.db import models
from datetime import datetime, timezone
from PIL import Image

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
    ('artist_name', 'Artist name'),
    ('album_name', 'Album name'),
    ('date_added', 'Date added'),
    ('track_name', 'Track name'),
    # ('manual', 'custom order')
]

GENRES = [
    ('rock', 'Rock'),
    ('hip hop', 'Hip hop music'),
    ('jazz', 'Jazz'),
    ('folk', 'Folk music'),
    ('pop', 'Pop music'),
    ('blues', 'Blues'),
    ('heavy metal', 'Heavy metal'),
    ('country', 'Country music'),
    ('classical', 'Classical music'),
    ('punk rock', 'Punk rock'),
    ('reggae', 'Reggae'),
    ('electronic', 'Electronic music'),
    ('techno', 'Techno'),
    ('funk', 'Funk'),
    ('alternative rock', 'Alternative rock'),
    ('indie rock', 'Indie rock'),
    ('hardcore', 'Hardcore'),
    ('ambient', 'Ambient music'),
    ('hardcore punk', 'Hardcore punk'),
    ('instrumental', 'Instrumental'),
    ('orchestra', 'Orchestra'),
    ('dubstep', 'Dubstep'),
    ('grunge', 'Grunge'),
    ('opera', 'Opera'),
    ('western', 'Western music'),
    ('progressive rock', 'Progressive rock'),
    ('other', 'Other')
]


def aware_utc_now():
    return datetime.now(timezone.utc)


class Profile(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, null=False, default='')
    description = models.TextField(max_length=2000, blank=True)
    profile_pic = models.ImageField(upload_to=f'userbase/', blank=True, null=False, default='')
    gender = models.CharField(max_length=20, choices=GENDER, blank=True, default='', null=False)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(150)], default=None, null=True)
    created_at = models.DateTimeField('date when the account was created', default=aware_utc_now)

    def __str__(self):
        # return f'{self.age} {self.gender} followers={self.followers}'
        return f'{self.first_name} {self.last_name}'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.profile_pic.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_pic.path)

class Userbase(Profile):
    username = models.CharField(max_length=32, unique=True, null=False, blank=False)
    password = models.CharField(max_length=64)
    # favourites = models.ForeignKey('Favourites', on_delete=models.CASCADE, related_name='+', default=create_fav)
    # profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='user')
    favourites = models.ManyToManyField('Track', through='FavouritesTracks')
    playlists = models.ManyToManyField('Playlist', through='UserbasePlaylists')
    followers = models.ManyToManyField('self', symmetrical=False, through='Followers',)


class Adminbase(Profile):
    username = models.CharField(max_length=32, unique=True, null=False, blank=False)
    password = models.CharField(max_length=64)
    level = models.CharField(max_length=1)
    
class Artist(Userbase):
    # first_name = models.CharField(max_length=200)
    # last_name = models.CharField(max_length=200, blank=True, null=False, default='')
    # description = models.TextField(max_length=2000, blank=True)
    # profile_pic = models.ImageField(upload_to=f'artist/', blank=True, null=False, default='')
    # secondary_images = models.ImageField(upload_to=f'artist_sec/{self.id}/', blank=True, null=False, default='')
    social_links = models.CharField(max_length=100, null=False, blank=True, default='')
    # profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.first_name +  ' ' +  self.last_name

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
    # below field is not updated when calling .update() on other fields
    # only auto updated when calling .save()
    last_modified_at = models.DateTimeField(auto_now=True,         
        verbose_name='store the last time when a track was added or removed from this playlist')
    # cant make owner a OneToOneField because it can be repeated(violates unique constraint)
    owner = models.ManyToManyField('Userbase')
    tracks = models.ManyToManyField('Track', through='TrackPlaylists')
    # favourites = models.ForeignKey('self', on_delete=models.CASCADE,)
        
    def __str__(self):
        return self.name + ' by ' + str(self.owner.get().username)


# def create_fav():
#     return Favourites.objects.create()

# class Favourites(Playlist): pass
# class Favourites(models.Model):
#     tracks = models.ManyToManyField('Track', through='FavouritesTracks')

class FavouritesTracks(models.Model):
    tracks = models.ForeignKey('Track', on_delete=models.CASCADE)
    user = models.ForeignKey('Userbase', on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=aware_utc_now)

class Followers(models.Model):
    leader = models.ForeignKey('Userbase', on_delete=models.CASCADE, related_name='followee')
    follower = models.ForeignKey('Userbase', on_delete=models.CASCADE, related_name='follower')

    def __str__(self):
        return 'Followers <object>'

class UserbasePlaylists(models.Model):
    write = models.BooleanField('whether user can edit playlists or not')
    userbase = models.ForeignKey('Userbase', on_delete=models.CASCADE)
    playlists = models.ForeignKey('Playlist', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.userbase.username} | {self.playlists.name}'

class TrackPlaylists(models.Model):
    track = models.ForeignKey('Track', on_delete=models.CASCADE)
    playlists = models.ForeignKey('Playlist', on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=aware_utc_now)

class Album(models.Model):
    title = models.CharField(max_length=200)
    released_at = models.DateTimeField(null=True)
    album_type = models.CharField('album or single', max_length=10)
    cover_image = models.ImageField(upload_to='album_covers/')
    artist = models.ManyToManyField('Artist')

    def __str__(self):
        return self.title

class Track(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50, choices=GENRES, default='other')
    released_at = models.DateTimeField(null=True)
    duration = models.PositiveIntegerField('duration of track in secs')
    explicit = models.BooleanField()
    created_at = models.DateTimeField('date when the track was uploaded', default=aware_utc_now)
    total_streams = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='track_covers/')
    album = models.ForeignKey('Album', on_delete=models.CASCADE, blank=False, null=True)
    artist = models.ManyToManyField('Artist')

    def __str__(self):
        return self.title


class Lyrics(models.Model):
    content = models.FileField(upload_to='lyrics/')

'''
python manage.py reset_db && python manage.py makemigrations && python manage.py migrate


# ======================== CREATE ========================

pp = "C:\\Users\\zznixt\\OneDrive\\innit_perhaps\\django_app\\django_testing_here\\media\\42.jfif"

# // create user in DB
zznix = Userbase.objects.create(first_name='Nisan', last_name='Thapa', gender='male', age=20, profile_pic=pp, username='zznix', password='1234')
kells = Userbase.objects.create(first_name='Nischal', last_name='Khatri', gender='male', age=20, profile_pic=pp, username='kells', password='1234')
lekha = Userbase.objects.create(first_name='Kamala', last_name='Thapa',gender='female', age=44, profile_pic=pp, username='lekha', password='brt')

# // add followers to a user
zznix.followers.add(lekha, kells)
kells.followers.add(zznix)

# // create playlist in DB
deez = Playlist.objects.create(name='deezloaderz', description='soundiiz')
catchy = Playlist.objects.create(name='catchy', description='kells playlist',)
nword = Playlist.objects.create(name='The N Word', description='nostalgia')

# // add a owner to a playlist.
deez.owner.add(zznix)
catchy.owner.add(kells)
nword.owner.add(zznix)

# // add playlists to user library.(Follow playlist)
lekha.playlists.add(deez, through_defaults={'write': True})
kells.playlists.add(deez, through_defaults={'write': False})
zznix.playlists.add(catchy, through_defaults={'write': False})

from datetime import datetime, timezone
dt = datetime.now(timezone.utc)
pp = "C:\\Users\\zznixt\\OneDrive\\innit_perhaps\\django_app\\django_testing_here\\media\\78.jfif"

# // add artists to DB
pilots = Artist.objects.create(first_name='21 Pilots', profile_pic=pp, username='21p', password='00',)
ryan = Artist.objects.create(first_name='Ryan', last_name='Tedder', gender='male', profile_pic=pp, username='rtedder', password='00',)
one_r = Artist.objects.create(first_name='One Republic', profile_pic=pp, username='@1Rp', password='00',)
tyler = Artist.objects.create(first_name='Tyler',gender='male', last_name='lyle', profile_pic=pp, username='tyler_lyle', password='00',)
andrew = Artist.objects.create(first_name='Andrew', gender='male', last_name='Bird', profile_pic=pp, username='bird_andrew', password='00',)
galantis = Artist.objects.create(first_name='Galantis', gender='female', profile_pic=pp, username='@galantis', password='00',)
midnight = Artist.objects.create(first_name='The Midnight', gender='female', profile_pic=pp, username='theMidnight', password='00',)

# // add followers to artists (same as above)
pilots.followers.add(zznix, kells)
one_r.followers.add(zznix)
andrew.followers.add(kells, lekha)
galantis.followers.add(lekha)
midnight.followers.add(kells)

# // add albums to DB
a1 = Album.objects.create(title='BlurryFace', released_at=dt, album_type='single', cover_image=pp)
a2 = Album.objects.create(title='Oh my my', released_at=dt, album_type='single', cover_image=pp)
a3 = Album.objects.create(title='My finest work yet', released_at=dt, album_type='single', cover_image=pp)
a4 = Album.objects.create(title='Naive', released_at=dt, album_type='album', cover_image=pp)
a5 = Album.objects.create(title='Bones', released_at=dt, album_type='album', cover_image=pp)

# // add artist(s) to album
a1.artist.add(pilots)
a2.artist.add(one_r)
a3.artist.add(andrew)
a4.artist.add(one_r)
a5.artist.add(one_r, galantis)

# // add tracks to DB (album is optional)
tear = Track.objects.create(title='Tear in my heart', album=a1, genre='rock', released_at=dt, duration=4, explicit=False, created_at=dt, total_streams=21, cover_image=pp)
stars = Track.objects.create(title='Counting Stars', album=a4, genre='pop', released_at=dt, duration=4, explicit=False, created_at=dt, total_streams=21, cover_image=pp)
sisyephus = Track.objects.create(title='Sisyephus', album=a3, genre='', released_at=dt, duration=4, explicit=False, created_at=dt, total_streams=21, cover_image=pp)
bones = Track.objects.create(title='Bones', album=a5, genre='pop', released_at=dt, duration=4, explicit=False, created_at=dt, total_streams=21, cover_image=pp)
stressed_out = Track.objects.create(title='Stressed Out', album=a1, genre='rock', released_at=dt, duration=5, explicit=False, created_at=dt, total_streams=100, cover_image=pp)
smth_i_need = Track.objects.create(title='Something I need', album=a4, genre='pop', released_at=dt, duration=4, explicit=False, created_at=dt, total_streams=21, cover_image=pp)

# // add artist(s) to tracks.
tear.artist.add(pilots)
stars.artist.add(one_r)
sisyephus.artist.add(andrew)
bones.artist.add(one_r, galantis)
stressed_out.artist.add(pilots)
smth_i_need.artist.add(one_r)

# // add track(s) to a playlist
deez.tracks.add(tear, bones, stressed_out, smth_i_need, through_defaults={'added_at': dt})
nword.tracks.add(stars, through_defaults={'added_at': dt})
catchy.tracks.add(sisyephus, stars, through_defaults={'added_at': dt})
# adding same tracks overwrites. check before overwrite ??
catchy.tracks.add(sisyephus, stars, through_defaults={'added_at': dt})

# // add track to Favourites
zznix.favourites.add(stars, smth_i_need)






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
# []
# means lekha has no followers

# // fetch a followers followings.
[e.leader.username for e in Followers.objects.filter(follower=lekha.id)]
lekha.userbase_set.all()
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

# --- UPDATE --

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

# // remove an artist
Artist.objects.get(id=4).delete()

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
has_write_permission = UserbasePlaylists.objects.get(id=1).write
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


'''


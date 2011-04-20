import datetime
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from lfm.helpers import Api
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
Api = Api()

# Create your models here.
class AbstractContent(models.Model):
    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        app_label = 'lfm'

class AbstractSimilar(AbstractContent):
    match = models.FloatField()
    def __unicode__(self):
        return '<%s> (%s%)'%(str(self.from_id),self.match)
    class Meta:
        abstract = True
        app_label = 'lfm'
        
class LFMContent(AbstractContent):
    tags = models.ManyToManyField("Tag")
    name = models.CharField(max_length=255, null=True, blank=True)
    tag_count = models.IntegerField(max_length=10, default=0)
    url = models.URLField(verify_exists=False, null=True, blank=True, max_length=500)
    mbid = models.CharField(max_length=36, null=True, blank=True)
    listeners = models.IntegerField(max_length=10, null=True, blank=True)
    global_playcount = models.IntegerField(max_length=10, null=True, blank=True)
    class Meta:
        abstract = True
        app_label = 'lfm'

class LFMContentU(AbstractContent):
    '''unique name field. TODO: Find a better way to do this'''
    tags = models.ManyToManyField("Tag")
    name = models.CharField(max_length=255, null=True, blank=True, unique=True)
    tag_count = models.IntegerField(max_length=10, default=0)
    url = models.URLField(verify_exists=False, null=True, blank=True, max_length=500)
    mbid = models.CharField(max_length=36, null=True, blank=True)
    listeners = models.IntegerField(max_length=10, null=True, blank=True)
    global_playcount = models.IntegerField(max_length=10, null=True, blank=True)
    class Meta:
        abstract = True
        app_label = 'lfm'
        
class Tag(AbstractContent):
    name = models.CharField(max_length=50)
    reach = models.IntegerField()
    summary = models.CharField(max_length=100)
    
class Image(AbstractContent):
    #always save the first one listed by default.
    '''
    u'image': [{u'#text': u'http://userserve-ak.last.fm/serve/34s/23226951.jpg',
                u'size': u'small'},
               {u'#text': u'http://userserve-ak.last.fm/serve/64s/23226951.jpg',
                u'size': u'medium'},
               {u'#text': u'http://userserve-ak.last.fm/serve/126/23226951.jpg',
                u'size': u'large'},
               {u'#text': u'http://userserve-ak.last.fm/serve/300x300/23226951.jpg',
                u'size': u'extralarge'}],
    
    '''
    url = models.URLField(max_length=500, verify_exists=False)

class Artist(LFMContentU):
    similar = models.ManyToManyField("self", through="SimilarArtist", symmetrical=False)
    image = models.ForeignKey(Image, blank=True, null=True)
    @classmethod
    def get_or_create(self, name):
        try:
            artist = Artist.objects.get(name=name)
        except ObjectDoesNotExist:
            resp = Api.artist_getinfo(name)
            artist_dict = resp.get('artist')
            artist = Artist(name=name)
            artist.lfm_url = artist_dict.get('url')
            artist.mbid = artist_dict.get('mbid')
            artist.listeners = artist_dict.get('stats').get('listeners')
            artist.global_playcount = artist_dict.get('stats').get('playcount')
            artist.save()
        return artist
    
    def __meta__(self):
        unique_together = ('name',)

    def __unicode__(self):
        return u'%s'%(self.name)
    
class Album(LFMContent):
    artist = models.ForeignKey(Artist, related_name='albums')
    images = models.ManyToManyField(Image)
    lfmid = models.CharField(max_length=25,null=True,blank=True)
    
class Track(LFMContent):
    artist = models.ForeignKey(Artist, related_name='tracks', null=True, blank=True)
    album = models.ForeignKey(Album, related_name='tracks', null=True, blank=True)
    similar = models.ManyToManyField("self", through="SimilarTrack", symmetrical=False)
    lfmid = models.CharField(max_length=25, null=True,blank=True)
    image = models.ForeignKey(Image, related_name='tracks', null=True, blank=True)
    duration = models.PositiveIntegerField(max_length=10, default=0)
    
    @classmethod
    def get_or_create(self, track_dict):
        try:
            track_name = track_dict.get('name')
            artist_name = track_dict.get('artist').get('name')
            track = Track.objects.get(name=track_name, artist__name=artist_name)
        except ObjectDoesNotExist:
            track = Track(name=track_dict.get('name'))
            track.url = track_dict.get('url')
            track.mbid = track_dict.get('mbid')

            track.artist = Artist.get_or_create(name=track_dict.get('artist').get('name'))
            track.duration = track_dict.get('duration') and int(track_dict.get('duration')) or 0

            image = None
            if track_dict.get('image') and len(track_dict.get('image')[0].get('#text')):
                image = Image(url=track_dict.get('image')[0].get('#text'))
                image.save()
            
            if image is not None:
                track.image = image

            track.save()
        return track

    def _get_addtl_info(self):
        resp = Api.track_getinfo(self.name, self.artist.name)
        track_dict = resp.get('track')
        self.album = None
        self.lfmid = track_dict.get('id')
        self.url = track_dict.get('ur')
        self.mbid = track_dict.get('mbid')
        self.listeners = track_dict.get('listeners')
        self.global_playcount = int(track_dict.get('playcount'))
        self.save()
        return True

    def get_addtl_info(self):
        from lfm.tasks import track_getinfo_task
        track_getinfo_task.apply_async([self.id, None])

    def __unicode__(self):
        if self.artist:
            return u'%s - %s (%s)'%(self.name, self.artist.name, self.duration/1000)
        else:
            return u'%s - %s (%s)'%(self.name, 'NO ARTIST', self.duration/1000)
    
class SimilarArtist(AbstractSimilar):
    from_id = models.ForeignKey(Artist,related_name='similar_to')
    to_id = models.ForeignKey(Artist,related_name='similar_from')
    
class SimilarTrack(AbstractSimilar):
    from_id = models.ForeignKey(Track,related_name='similar_to')
    to_id = models.ForeignKey(Track,related_name='similar_from')

class UserTrack(AbstractContent):
    user_profile = models.ForeignKey("UserProfile")
    track = models.ForeignKey(Track)
    location = models.CharField(max_length=50,blank=True,null=True)
    personal_playcount = models.IntegerField(max_length=5)
    
class Playlist(AbstractContent):
    tracks = models.ManyToManyField('Track')
    name = models.CharField(max_length=255)
    ordering = models.CommaSeparatedIntegerField(max_length=500)
    
class UserProfile(AbstractContent):
    tracks = models.ManyToManyField(Track, through="UserTrack")
    lfm_username = models.CharField(max_length=36, unique=True)
    track_pages_loaded = models.CharField(max_length=500, blank=True)
    friends = models.ManyToManyField("UserProfile")
    tracks_week = models.ManyToManyField(Track, through="UserTrackWeek", related_name="userprofile_week_set")
    tracks_week_updated_at = models.DateTimeField(blank=True, null=True)
    updating_track_week = models.BooleanField(default=False)
    updated_friends_at = models.DateTimeField(blank=True, null=True)
    visited = models.BooleanField(default=False)
    def __unicode__(self):
        return u'%s'%self.lfm_username
    
    def _update_trackweek(self, page=1):
        print 'INSIDE _UPDATE_TRACKWEEK'
        resp = Api.user_get_toptracks_week(self.lfm_username, page)
        if page == 1:
            from lfm.tasks import update_trackweek_task
            attr = resp['toptracks'].get('@attr')
            if attr is None:
                maxpages = 2
            else:
                maxpages = int(attr.get('totalPages'))+1
            for page_num in range(2, maxpages):
                update_trackweek_task.apply_async([self.id, page_num])
        tracks = resp.get('toptracks').get('track')
        if tracks is None:
            return
        elif isinstance(tracks, list):
            for track in tracks:
                UserTrackWeek.create(self, track)
            
        elif isinstance(tracks, dict):
            Track.make_trackweek(self, tracks) #TODO: add this classmethod to the track class

        if int(resp['toptracks']['@attr']['page']) == int(resp['toptracks']['@attr']['totalPages']):
            self.updating_track_week = False
            self.tracks_week_updated_at = datetime.datetime.now()
            self.save()

    def update_trackweek(self):
        print 'INSIDE UPDATE_TRACKWEEK'
        if self.updating_track_week:
            print 'WARNING: %s is already updating their trackweek. Failure'%self
            return False
        elif self.tracks_week_updated_at == None or datetime.datetime.now() - self.tracks_week_updated_at > datetime.timedelta(7):
            print 'Changing updating_track_week for %s'%self
            self.updating_track_week = True
            self.usertrackweek_set.all().delete()
            self.save()
            from lfm.tasks import update_trackweek_task
            update_trackweek_task.apply_async([self.id])
        
    def update_friends_data(self):
        self.update_trackweek()
        for friend in self.friends.all():
            friend.update_trackweek()
        
    def _update_friends(self, page=1):
        '''user is a UserProfile object'''
        print 'getting friends page for %s'%self
        from lfm.tasks import update_friends_task
        resp = Api.user_getfriends(self.lfm_username, page=page)
        for friend_data in resp.get('friends').get('user'):
            (friend,created) = UserProfile.objects.get_or_create(lfm_username=friend_data.get('name'))
            self.friends.add(friend)
            print 'added friend',friend
        
        if page == 1:
            total_pages = int(resp.get('friends').get('@attr').get('totalPages'))
            for page_num in range(2,total_pages+1):
                update_friends_task.wait([self.id, page_num])
            self.update_friends_data()
    
    def update_friends(self):
        from lfm.tasks import update_friends_task
        update_friends_task.apply_async([self.id, 1])
        print 'update_friends called'
        
    def _get_addtl_info(self):
        pass
        #resp = Api.user_getinfo(self.lfm_username)
        #self.image = Image


    def get_addtl_info(self):
        '''stuff like image, real name, etc'''
        from lfm.tasks import userprofile_getinfo_task
        userprofile_getinfo_task.apply_async([self.id, None])
    
class UserTrackWeek(AbstractContent):
    user_profile = models.ForeignKey("UserProfile")
    track = models.ForeignKey(Track)
    personal_playcount = models.IntegerField(max_length=5)
    
    def __unicode__(self):
        if self.track and self.track.artist:
            return u'%s - %s - %s times'%(self.track.name, self.track.artist.name, self.personal_playcount)
        else:
            return u'%s - NO ARTIST - %s times'%(self.track.name, self.personal_playcount)
    
    @classmethod
    def create(self, user, track_dict):
        track = Track.get_or_create(track_dict)
        usertrackweek = UserTrackWeek(track=track, 
                personal_playcount=track_dict.get('playcount'),
                user_profile=user)
        usertrackweek.save()
        return True


@receiver(post_save, sender=UserProfile, dispatch_uid="userprofile_postsave")
def userprofile_postsave(*args, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        if instance.visited:
            instance.update_friends()
        instance.update_trackweek()
        instance.get_addtl_info()
        
@receiver(post_save, sender=Track, dispatch_uid='track_postsave')
def track_postsave(*args, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        instance.get_addtl_info()

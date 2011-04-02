from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

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
    name = models.CharField(max_length=255, null=True, blank=True)
    tags = models.ManyToManyField("Tag")
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

class Artist(LFMContent):
    similar = models.ManyToManyField("self", through="SimilarArtist", symmetrical=False)
    image = models.ForeignKey(Image, blank=True, null=True)
    
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
    
class UserProfile(AbstractContent):
    tracks = models.ManyToManyField(Track, through="UserTrack")
    lfm_username = models.CharField(max_length=36, unique=True)
    track_pages_loaded = models.CharField(max_length=500, blank=True)
    friends = models.ManyToManyField("UserProfile")
    tracks_week = models.ManyToManyField(Track, through="UserTrackWeek", related_name="userprofile_week_set")
    
    def __unicode__(self):
        return u'%s'%self.lfm_username
    
class UserTrackWeek(AbstractContent):
    user_profile = models.ForeignKey("UserProfile")
    track = models.ForeignKey(Track)
    personal_playcount = models.IntegerField(max_length=5)
    
    def __unicode__(self):
        if self.track and self.track.artist:
            return u'%s - %s - %s times'%(self.track.name, self.track.artist.name, self.personal_playcount)
        else:
            return u'%s - NO ARTIST - %s times'%(self.track.name, self.personal_playcount)
# @receiver(post_save, sender=Artist)
# def postsave_callback(sender, **kwargs):
#     pass
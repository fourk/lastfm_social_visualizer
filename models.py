from django.db import models
from django.contrib.auth.models import User

class AbstractContent(models.Model):
	objects = models.Manager()
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)
	class Meta:
		abstract = True
		app_label = 'rb'
		
class UserProfile(AbstractContent):
	user = models.ForeignKey(User,unique=True,null=True,blank=True)
	lfmusername = models.CharField(max_length=25)
	artists = models.ManyToManyField('Artist',blank=True,through='UserArtist')
	processed = models.DateTimeField(null=True,blank=True)
	pages_loaded = models.CharField(max_length=120,null=True,blank=True)
	
	
class Track(AbstractContent):
	name = models.CharField(max_length=100)
	artist = models.ForeignKey('Artist',related_name='tracks')
	cover = models.BooleanField()
	decade = models.CharField(max_length=4)
	difficulty_band = models.IntegerField()
	difficulty_bass = models.IntegerField()
	difficulty_drums = models.IntegerField()
	difficulty_guitar = models.IntegerField()
	difficulty_keys = models.IntegerField()
	difficulty_pro_bass = models.IntegerField()
	difficulty_pro_drums = models.IntegerField()
	difficulty_pro_guitar = models.IntegerField()
	difficulty_pro_keys = models.IntegerField()
	difficulty_vocals = models.IntegerField()
	genre_symbol = models.CharField(max_length=20) #[u'metal', u'blues', u'rbsoulfunk', u'reggaeska', u'numetal', u'novelty', u'other', u'prog', u'urban', u'alternative', u'grunge', u'jazz', u'poprock', u'glam', u'indierock', u'new_wave', u'country', u'emo', u'punk', u'southernrock', u'rock', u'classicrock']
	rating = models.CharField(max_length=1) #['1','2','4']   ---- associated with 'Family Friendly', 'Supervision Required', and 'No Rating'
	source = models.CharField(max_length=20) #set([u'DLC', u'GDRB', u'LEGO', u'RB3', u'RB2', u'RB1', u'RBN'])
	vocal_parts = models.CharField(max_length=1) #set([u'1', u'0', u'3', u'2'])
	year_released = models.CharField(max_length=4,blank=True,null=True) #set([u'1974', u'1965', None, u'1977', u'1986', u'1987', u'1984', u'1985', u'1982', u'1983', u'1980', u'1981', u'1979', u'1966', u'1967', u'1988', u'1989', u'2011', u'2010', u'1998', u'1968', u'1969', u'1991', u'1990', u'1993', u'1992', u'1995', u'1994', u'1997', u'1996', u'1999', u'1976', u'1975', u'1978', u'1973', u'1972', u'1971', u'1970', u'2002', u'2003', u'2000', u'2001', u'2006', u'2007', u'2004', u'2005', u'2008', u'2009'])
	shortname = models.CharField(max_length=35)
#	cover = models.BooleanField(null=True)
	
class UserArtist(AbstractContent):
	useraccount = models.ForeignKey('UserProfile')
	artist = models.ForeignKey('Artist')
	listens = models.IntegerField()
	class Meta:
		unique_together = ('useraccount','artist')
	
class Artist(AbstractContent):
	name = models.CharField(max_length=100)
'''
Created on Nov 8, 2010

@author: jburkhart
'''
from django.conf import settings
from rb.models import Artist,UserProfile,UserArtist
from django_beanstalkd import BeanstalkClient
from django.core.exceptions import ObjectDoesNotExist 
import datetime
try:
	import json
except ImportError:
	import simplejson as json
import time
import urllib2
API = settings.API
def get_for_user(username):
	try:
		user = UserProfile.objects.get(lfmusername=username)
		client = BeanstalkClient()
		response = get_page(username=username)
		info = response['artists']['@attr']
		handle_resp(user,response)
		for page in range(2,int(info.get('totalPages'))+1):
			job_data = {'uname':username,'page':page}
			client.call('rb.processpage',json.dumps(job_data))
		user.processed = datetime.datetime.now()
		user.save()
	except Exception, e:
		if settings.DEBUG:
			raise
		f=open(settings.LOG_DIRECTORY+"getforuser","a")
		f.write(str(e)+'\n')
		f.close()
	
def handle_resp(user,resp):
	artists = resp['artists']['artist']
	for artist in artists:
		make_artist(user,artist)
	pagecomplete = int(resp['artists']['@attr']['page'])
	if not user.pages_loaded:
		user.pages_loaded = '0'*int(resp['artists']['@attr']['totalPages'])
	user.pages_loaded = user.pages_loaded[:pagecomplete-1]+'1'+user.pages_loaded[pagecomplete:]
	user.save()
	
def get_url(username,page=1):
	return 'http://ws.audioscrobbler.com/2.0/?method=library.getartists&api_key=%s&user=%s&format=json&page=%s'%(API,username,page)

def get_page(username,page=1):
	print 'PAGENUMBER',page
	reply = urllib2.urlopen(get_url(username,page))
	return json.loads(reply.read())

def make_artist(user,artist):
	'''user is a UserProfile object,
	artist is the json object returned by lastfm, of the following format:
	{u'image': [{u'#text': u'http://userserve-ak.last.fm/serve/34/9269.jpg',
             u'size': u'small'},
            {u'#text': u'http://userserve-ak.last.fm/serve/64/9269.jpg',
             u'size': u'medium'},
            {u'#text': u'http://userserve-ak.last.fm/serve/126/9269.jpg',
             u'size': u'large'},
            {u'#text': u'http://userserve-ak.last.fm/serve/252/9269.jpg',
             u'size': u'extralarge'},
            {u'#text': u'http://userserve-ak.last.fm/serve/500/9269/Ratatat.jpg',
             u'size': u'mega'}],
	 u'mbid': u'f467181e-d5e0-4285-b47e-e853dcc89ee7',
	 u'name': u'Ratatat',
	 u'playcount': u'780',
	 u'streamable': u'1',
	 u'tagcount': u'0',
	 u'url': u'http://www.last.fm/music/Ratatat'}
	 '''
	try:
		print artist.get('name')
	except:
		print 'error!'
	try:
		a = Artist.objects.get(name=artist.get('name'))
	except ObjectDoesNotExist:
		a = Artist(name=artist.get('name'))
		a.save()
	try:
		relation = UserArtist.objects.get(useraccount=user, artist=a)
	except ObjectDoesNotExist:
		relation = UserArtist(useraccount=user, artist=a)
	relation.listens = int(artist.get('playcount')) 
	relation.save()
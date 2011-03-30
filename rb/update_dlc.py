'''
Created on Nov 8, 2010

@author: jburkhart
'''
import urllib2
try:
	import simplejson as json
except:
	import json
from django.core.exceptions import ObjectDoesNotExist 
from rb.models import Track,Artist

def get_all():
	resp = urllib2.urlopen('http://www.rockband.com/services.php/music/all-songs.json')
	resp = json.loads(resp.read())
	handle_resp(resp)
	
def handle_resp(resp):
	for track_data in resp:
		try:
			track = Track.objects.get(shortname=track_data.get('shortname'))
		except ObjectDoesNotExist:
			try:
				artist = Artist.objects.get(name=track_data.get('artist_tr'))
			except ObjectDoesNotExist:
				artist = Artist(name=track_data.get('artist_tr'))
				artist.save()
			finally:
				track = Track(name = track_data.get('name'),
					artist = artist,
					cover = True if track_data.get('cover') == 't' else False,
					decade = track_data.get('decade'),
					difficulty_band = track_data.get('difficulty_band'),
					difficulty_bass = track_data.get('difficulty_bass'),
					difficulty_drums = track_data.get('difficulty_drums'),
					difficulty_guitar = track_data.get('difficulty_guitar'),
					difficulty_keys = track_data.get('difficulty_keys'),
					difficulty_pro_bass = track_data.get('difficulty_pro_bass'),
					difficulty_pro_drums = track_data.get('difficulty_pro_drums'),
					difficulty_pro_guitar = track_data.get('difficulty_pro_guitar'),
					difficulty_pro_keys = track_data.get('difficulty_pro_keys'),
					difficulty_vocals = track_data.get('difficulty_vocals'),
					genre_symbol = track_data.get('genre_symbol'),
					rating = track_data.get('rating'),
					source = track_data.get('source'),
					vocal_parts = track_data.get('vocal_parts'),
					year_released = track_data.get('year_released'),
					shortname = track_data.get('shortname'),
					)
				track.save()
				

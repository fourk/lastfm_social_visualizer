# Create your views here.
from django.core.exceptions import ObjectDoesNotExist 
from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
import operator
from lfm.models import UserProfile, Track

import gdata.youtube
import gdata.youtube.service

try:
	import json
except ImportError:
	import simplejson as json
	
SERVICE = gdata.youtube.service.YouTubeService()

def init_service():
    global SERVICE
    SERVICE.ssl = False
    SERVICE.developer_key = "AI39si5gXMVIPK2a48hTLPj9lJTYrpqIBHyDYX57krStY63u14jwuo5H0jUq3DK5-0lb7ZPQISQL8px85CnXrcAXbFRqS6lpPw"
    
#17 color support.
COLORS = ['DC143C', 'FFB6C1', '8B5F65', 'EE799F', '9F79EE', '483D8B', '0000FF', '3D59AB', '6CA6CD', '00C78C', '2E8B57', '98FB98', '698B22', 'BDB76B', 'EE9A00', 'EEC591', '6E6E6E'] #these are arranged in the order i found them on http://cloford.com/resources/colours/500col.htm
COLORS = ['#98FB98', '#00C78C', '#3D59AB', '#BDB76B', '#FFB6C1', '#EE9A00', '#0000FF', '#483D8B', '#DC143C', '#698B22', '#EE799F', '#8B5F65', '#6E6E6E', '#EEC591', '#9F79EE', '#2E8B57', '#6CA6CD']
def foo(request):
    return render(request, 'lfm/top100.html')

def PrintEntryDetails(entry):
  print 'Video title: %s' % entry.media.title.text
  print 'Video published on: %s ' % entry.published.text
  print 'Video description: %s' % entry.media.description.text
  print 'Video category: %s' % entry.media.category[0].text
  print 'Video tags: %s' % entry.media.keywords.text
  print 'Video watch page: %s' % entry.media.player.url
  print 'Video flash player URL: %s' % entry.GetSwfUrl()
  print 'Video duration: %s' % entry.media.duration.seconds

  # non entry.media attributes
  # print 'Video geo location: %s' % entry.geo.location()
  print 'Video view count: %s' % entry.statistics.view_count
  print 'Video rating: %s' % entry.rating.average
  
  print '================================================'
  print
  # show alternate formats
  for alternate_format in entry.media.content:
    if 'isDefault' not in alternate_format.extension_attributes:
      print 'Alternate format: %s | url: %s ' % (alternate_format.type,
                                                 alternate_format.url)

  # show thumbnails
  for thumbnail in entry.media.thumbnail:
    print 'Thumbnail url: %s' % thumbnail.url

def PrintVideoFeed(feed):
  for entry in feed.entry:
    PrintEntryDetails(entry)
    
def youtube(request, id):
    try:
        query = gdata.youtube.service.YouTubeVideoQuery()
        track = Track.objects.get(id=id)
        query.vq = '%s - %s'%(track.name, track.artist.name)
        query.orderby = 'relevance'
        query.racy = 'include'
        feed = SERVICE.YouTubeQuery(query)
        video_id = feed.entry[0].id.text.rsplit('/')[-1]
        return HttpResponse(video_id)
    except Exception, e:
        print e
        return HttpResponse('error')
    
def get_top100(request):
    username = request.GET.get('username')
    retval = None
    retval = cache.get('testing')

    if retval is None:
        (resp,listeners) = helper(username)
    
        resp = resp[:100]
        user_list = []
        user_hash = {}
        for user in listeners:
            user_hash[user.lfm_username] = COLORS.pop()
            user_list.append(user.lfm_username)
    
        for artist_dict in resp:
            for listener_dict in artist_dict.get('listeners'):
                listener_dict['listens'].sort(key=lambda x:x.track.duration * x.personal_playcount, reverse=True)
                listener_dict['listens'] = [{'name': k.track.name, 
                            'playcount': k.personal_playcount, 
                            'duration': k.track.duration * k.personal_playcount / 1000,
                            'id': k.track.id,
                            } for k in listener_dict['listens']]
                listener_dict['user'] = listener_dict['user'].lfm_username
            
            tracks = []
            for track_key in artist_dict.get('tracks'):
                track_dict = artist_dict['tracks'][track_key]
                tracks.append({'name':track_key, 
                        'duration':track_dict.get('sum_duration'), 
                        'playcount':track_dict.get('sum_playcount'),
                        'listens': [{'user':listen.user_profile.lfm_username, 'playcount':listen.personal_playcount, 'id':listen.track.id} for listen in track_dict.get('listens')],
                        'id': track_dict.get('id'),
                        })
            tracks.sort(key=lambda x:x.get('duration'), reverse=True)
            artist_dict['tracks'] = tracks
            artist_dict['listens'] = []
    
        retval = json.dumps({'lfmData':resp, 'userHash':user_hash, 'userList':user_list})
        cache.set('testing', retval, 60*60*4)

    return HttpResponse(retval)
    
def helper(username, friends=True):
    try:
        user = UserProfile.objects.get(lfm_username=username)
        
    except ObjectDoesNotExist:
        return {'error': 'fuck, man.'}
        #TODO: handle this.
    listens = []
    if friends:
        [listens.append(listen) for friend in user.friends.all() for listen in friend.usertrackweek_set.all()]
    listens.extend(user.usertrackweek_set.all())
        
    tracks = [listen.track for listen in listens]
    artists = set([track.artist for track in tracks])
    artist_hash = {}
    
    if artists is None:
        return []
            
    for artist in artists:
        if artist:
            artist_hash[artist.name] = {'sum_duration': 0,
                    'tracks': {},
                    'listens': [],
                    'artist_name': artist.name,
                    'artist_img': artist.image and artist.image.url or '',
                    'listeners': [],
                    }
    
    for listen in listens:
        if listen.track.artist:
            artist_hash[listen.track.artist.name]['listens'].append(listen)#TODO
            artist_hash[listen.track.artist.name]['sum_duration'] += listen.track.duration/1000 * listen.personal_playcount
            if artist_hash[listen.track.artist.name]['artist_img'] == '' and listen.track.artist.image:
                artist_hash[listen.track.artist.name]['artist_img'] = listen.track.artist.image.url;
                #i think this code is both terrible and broken.
        
    # for track in tracks:
    #     hash[track.artist.name]['tracks'].append(track)
    #     hash[track.artist.name]['sum_duration'] += track.duration
    all_listeners = []
    ls = []
    
    for k in artist_hash:
        listeners = set([listen.user_profile for listen in artist_hash[k].get('listens')])
        all_listeners.extend(listeners)
        for listener in listeners:
            user_listens = [listen for listen in artist_hash[k].get('listens') if listen.user_profile == listener]
            artist_hash[k]['listeners'].append({
                    'user': listener,
                    'listens': user_listens,
                    'listening_duration': sum([listen.track.duration for listen in user_listens])/1000
                    })
        artist_hash[k]['listeners'].sort(key=lambda x:x.get('listening_duration'), reverse=True)
        tracks = list(set([listen.track.name for listen in artist_hash[k].get('listens')]))
        for track in tracks:
            artist_hash[k]['tracks'][track] = {'listens':[], 'sum_duration':0, 'sum_playcount':0, 'id': None}
            try:
                artist_hash[k]['tracks'][track]['id'] = Track.objects.get(name=track).id
            except Exception, e:
                print e
        for listen in artist_hash[k].get('listens'):
            artist_hash[k]['tracks'][listen.track.name]['listens'].append(listen)
            artist_hash[k]['tracks'][listen.track.name]['sum_playcount']+=listen.personal_playcount
            artist_hash[k]['tracks'][listen.track.name]['sum_duration']+= listen.personal_playcount * listen.track.duration /1000
        ls.append(artist_hash[k])

    ls.sort(key=operator.itemgetter('sum_duration'), reverse=True)
    
    return (ls, set(all_listeners))

# def helper2(username):
#     try:
#         user = UserProfile.objects.get(lfm_username=username)
#         
#     except ObjectDoesNotExist:
#         return {'error': 'fuck, man.'}
#         #TODO: handle this.
#     ls = []
#     for friend in user.friends.all():
#         ls.append({'user':friend, 'data':helper(friend.lfm_username)}) THIS PART IS BROKEN NOW
#         
#     return ls
    
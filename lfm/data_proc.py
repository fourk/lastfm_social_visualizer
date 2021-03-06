'''
Created on Nov 8, 2010

@author: jburkhart
'''
from django.db import reset_queries, close_connection
from django.conf import settings
from lfm.models import Artist, UserTrack, UserProfile, Track, Image, UserTrackWeek
from django_beanstalkd import BeanstalkClient
from django.core.exceptions import ObjectDoesNotExist 


from unidecode.unidecoder import Unidecoder
try:
    import json
except ImportError:
    import simplejson as json

import urllib2

API = settings.API
CLIENT = BeanstalkClient()
DECODER_RING = Unidecoder()

def get_for_user(username, week=False):
    print 'Going to get for user %s, week: %s'%(username, week)
    try:
        user = UserProfile.objects.get(lfm_username=username)
        
        response = get_page(username=username, page=1, week=week)
        has_tracks = process_page(user, response, week=week) #this returns False when the user has no tracks
        
        if has_tracks:
            key = week and 'toptracks' or 'tracks'
            for page in range(2, int(response[key]['@attr'].get('totalPages'))+1):
                job_data = {'uname':username, 'page':page, 'week':week}
                CLIENT.call('lfm.process_track_page', json.dumps(job_data))
        
    except Exception, e:
        if settings.DEBUG:
            raise
        f = open(settings.LOG_DIRECTORY+"getforuser","a")
        f.write(str(e) + '\n')
        f.close()
    
def process_page(user, resp, week=False):
    '''user is a UserProfile object'''
    key = week and 'toptracks' or 'tracks'
    tracks = resp[key].get('track')
    
    if tracks is None:
        print 'No tracks for this user!'
        return False

    if isinstance(tracks, list):
        for track in tracks:
            make_track(user, track, week=week)
    elif isinstance(tracks, dict):
        make_track(user, tracks, week=week)
    else:
        raise Exception('EXCEPTION WTF!? %s'%tracks)
    if not week:
        pagecomplete = int(resp['tracks']['@attr']['page'])

        if not user.track_pages_loaded:
            user.track_pages_loaded = '0'*int(resp['tracks']['@attr']['totalPages'])
    
        else:
            #TODO: replace this bit with transactions
            reset_queries()
            close_connection()
    
        user.track_pages_loaded = user.track_pages_loaded[:pagecomplete-1]+'1'+user.track_pages_loaded[pagecomplete:]
        user.save()
    else:
        pagecomplete = int(resp['toptracks']['@attr']['page'])
        if pagecomplete == int(resp['toptracks']['@attr']['totalPages']):
            user.updating_track_week = False
            user.save()
    return True
    
# def get_track_info_url(track, artist):
#     '''track and artist are strings'''
#     return 'http://ws.audioscrobbler.com/2.0/?method=track.getinfo&api_key=%s&track=%s&artist=%s&format=json'%(API, urllib2.quote(track.encode('utf-8')), urllib2.quote(artist.encode('utf-8')))
#     
# def get_week_url(username, page=1):
#     return 'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&period=7day&api_key=%s&user=%s&format=json&page=%s'%(API, username, page)
#     
# def get_url(username, page=1):
#     #library.gettracks
#     url = 'http://ws.audioscrobbler.com/2.0/?method=library.gettracks&api_key=%s&user=%s&format=json&page=%s'%(API, username, page)
#     return url
#     
# def get_friends_url(username, page=1):
#     #user.getfriends
#     return 'http://ws.audioscrobbler.com/2.0/?method=user.getfriends&api_key=%s&user=%s&format=json&page=%s'%(API, username, page)
# 
# def get_url_artist_getinfo(artist_name):
#     url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&api_key=%s&artist=%s&format=json'%(API, urllib2.quote(artist_name.encode('utf-8')))
#     return url
# 
# def get_page(username, page=1, week=False):
#     print 'PAGENUMBER',page
#     if week:
#         url = get_week_url(username, page)
#     else:
#         url = get_url(username, page)
#     
#     reply = urllib2.urlopen(url)
#     return json.loads(reply.read())

def make_track(user, track, week=False):
    '''user is a UserProfile object,
    track is the json object returned by lastfm, of the following format:
    {u'album': {u'name': u'Classics', u'position': u''},
     u'artist': {u'mbid': u'f467181e-d5e0-4285-b47e-e853dcc89ee7',
                 u'name': u'Ratatat',
                 u'url': u'http://www.last.fm/music/Ratatat'},
     u'duration': u'225000',
     u'image': [{u'#text': u'http://userserve-ak.last.fm/serve/34s/45788553.png',
                 u'size': u'small'},
                {u'#text': u'http://userserve-ak.last.fm/serve/64s/45788553.png',
                 u'size': u'medium'},
                {u'#text': u'http://userserve-ak.last.fm/serve/126/45788553.png',
                 u'size': u'large'},
                {u'#text': u'http://userserve-ak.last.fm/serve/300x300/45788553.png',
                 u'size': u'extralarge'}],
     u'mbid': u'',
     u'name': u'Loud Pipes',
     u'playcount': u'64',
     u'streamable': {u'#text': u'0', u'fulltrack': u'0'},
     u'tagcount': u'0',
     u'url': u'http://www.last.fm/music/Ratatat/_/Loud+Pipes'}
     '''
    try:
        print track.get('name'),'|',
    except Exception, e:
        print 'error printing track.get("name")!'
        try:
            print e
        except:
            print 'DOUBLE ERROR RAINBOW'
    try:
        t = Track.objects.get(name=track.get('name'))
        
        image = None
        if track.get('image') and len(track.get('image')[0].get('#text')):
            image = Image(url=track.get('image')[0].get('#text'))
            image.save()
    
        if image is not None:
            t.image = image
            
    except ObjectDoesNotExist:
        t = Track(name=track.get('name'))
        t.url = track.get('url')
        t.mbid = track.get('mbid')
        t.duration = track.get('duration') and int(track.get('duration')) or 0
        t.artist = get_or_create_artist(track.get('artist').get('name'))
        
        job_data = {'track_name':track.get('name'),
                    'artist_name':track.get('artist').get('name')}
        CLIENT.call('lfm.get_track_info', json.dumps(job_data))
            
        if not week:
            t.tag_count = int(track.get('tagcount'))

        t.save()
        
    #TODO: add a MoreThanOneObjectReturned except clause here

    relation_type = week and UserTrackWeek or UserTrack

    try:
        relation = relation_type.objects.get(user_profile=user, track=t)
    except ObjectDoesNotExist:
        relation = relation_type(user_profile=user, track=t)
        
    relation.personal_playcount = int(track.get('playcount'))
    relation.save()
    
    
    # if int(track.get('tagcount')):
    #     job_data = {'track_id': track.id}
    #     CLIENT.call('lfm.process_tags_for_track', json.dumps(job_data))
        

def get_or_create_artist(artist_name):
    '''artist_dict is of the following format:
    {u'mbid': u'a33a9cd6-8c03-4047-b62d-59f76f494c20',
         u'name': u'Cloud Cult',
         u'url': u'http://www.last.fm/music/Cloud+Cult'}'''
    try:
        artist = Artist.objects.get(name=artist_name)
        return artist
        
    except ObjectDoesNotExist:
        url = get_url_artist_getinfo(artist_name)
        reply = urllib2.urlopen(url)
        resp = json.loads(reply.read())
        
        artist = Artist(name=artist_name)
        
        
        artist.lfm_url = resp.get('artist').get('url')
        artist.mbid = resp.get('artist').get('mbid')
        artist.listeners = resp.get('artist').get('stats').get('listeners')
        artist.global_playcount = resp.get('artist').get('stats').get('playcount')
        artist.save()
        return artist
        '''
        {u'artist': {u'bio': {u'content': u'1. Girl Talk is the stage name of <a href="http://www.last.fm/music/Gregg+Gillis" class="bbcode_artist">Gregg Gillis</a> (born October 26, 1981). Gillis, who is based in Pittsburgh, Pennsylvania, has released five CD albums on <a href="http://www.last.fm/label/Illegal+Art/" class="bbcode_label">Illegal Art</a> and vinyl releases on 333 and 12 Apostles. He began making music while a student at Case Western Reserve University. He specializes in sample-based remixes, in which he uses at least a dozen elements from different songs to create a new song. At his early shows, Gillis became notorious for his exhibitionist antics on stage, spontaneously removing most or all of his clothing mid-performance. He has given different explanations for the origin of his stage name, once saying it alluded to a <a href="http://www.last.fm/music/Jim+Morrison" class="bbcode_artist">Jim Morrison</a> poem and once saying it alluded to an early <a href="http://www.last.fm/music/Merzbow" class="bbcode_artist">Merzbow</a> side project. He has also stated that &quot;Girl Talk&quot; is simply the opposite of what one would think when picturing a man playing music with a laptop. \n \n Girl Talk was featured in Good Copy Bad Copy and Rip! A Remix Manifesto; both documentary films about copyright/fair use.\n \n 2. Girl Talk is also the name of a British 80\'s eurodisco duo consisting of sisters Karen &amp; Julie Wright.\n \n \n    \nUser-contributed text is available under the Creative Commons By-SA License and may also be available under the GNU FDL.',
                              u'published': u'Mon, 15 Nov 2010 18:40:17 +0000',
                              u'summary': u'1. Girl Talk is the stage name of <a href="http://www.last.fm/music/Gregg+Gillis" class="bbcode_artist">Gregg Gillis</a> (born October 26, 1981). Gillis, who is based in Pittsburgh, Pennsylvania, has released five CD albums on <a href="http://www.last.fm/label/Illegal+Art/" class="bbcode_label">Illegal Art</a> and vinyl releases on 333 and 12 Apostles. He began making music while a student at Case Western Reserve University. He specializes in sample-based remixes, in which he uses at least a dozen elements from different songs to create a new song.'},
                     u'image': [{u'#text': u'http://userserve-ak.last.fm/serve/34/7003439.jpg',
                                 u'size': u'small'},
                                {u'#text': u'http://userserve-ak.last.fm/serve/64/7003439.jpg',
                                 u'size': u'medium'},
                                {u'#text': u'http://userserve-ak.last.fm/serve/126/7003439.jpg',
                                 u'size': u'large'},
                                {u'#text': u'http://userserve-ak.last.fm/serve/252/7003439.jpg',
                                 u'size': u'extralarge'},
                                {u'#text': u'http://userserve-ak.last.fm/serve/500/7003439/Girl+Talk+52014girltalksmall.jpg',
                                 u'size': u'mega'}],
                     u'mbid': u'24e36781-1f4a-40af-bd18-c5de61f10c66',
                     u'name': u'Girl Talk',
                     u'similar': {u'artist': [{u'image': [{u'#text': u'http://userserve-ak.last.fm/serve/34/26986787.jpg',
                                                           u'size': u'small'},
                                                          {u'#text': u'http://userserve-ak.last.fm/serve/64/26986787.jpg',
                                                           u'size': u'medium'},
                                                          {u'#text': u'http://userserve-ak.last.fm/serve/126/26986787.jpg',
                                                           u'size': u'large'},
                                                          {u'#text': u'http://userserve-ak.last.fm/serve/252/26986787.jpg',
                                                           u'size': u'extralarge'},
                                                          {u'#text': u'http://userserve-ak.last.fm/serve/_/26986787/Super+Mash+Bros+If+these+guys+are+going+to+be.jpg',
                                                           u'size': u'mega'}],
                                               u'name': u'Super Mash Bros.',
                                               u'url': u'http://www.last.fm/music/Super+Mash+Bros.'},
                                                {
                                                    ....more here.gk
                                                }
                                              ]},
                     u'stats': {u'listeners': u'325861', u'playcount': u'19560353'},
                     u'streamable': u'1',
                     u'tags': {u'tag': [{u'name': u'mashup',
                                         u'url': u'http://www.last.fm/tag/mashup'},
                                        {u'name': u'electronic',
                                         u'url': u'http://www.last.fm/tag/electronic'},
                                        {u'name': u'dance',
                                         u'url': u'http://www.last.fm/tag/dance'},
                                        {u'name': u'hip-hop',
                                         u'url': u'http://www.last.fm/tag/hip-hop'},
                                        {u'name': u'mash-up',
                                         u'url': u'http://www.last.fm/tag/mash-up'}]},
                     u'url': u'http://www.last.fm/music/Girl+Talk'}}'''
                     
def do_call(url):
    print '%s'%url
    return json.loads(urllib2.urlopen(url).read())
    
def get_friends_data(user):
    '''user is a UserProfile object'''
    print 'Getting friend data for %s'%user
    for friend in user.friends.all():
        job_data = {'username':user.lfm_username}
        CLIENT.call('lfm.get_user_track_week', json.dumps(job_data))
    
    
def process_friend_page(user, resp):
    print 'processing friend page for %s'%user
    '''user is a UserProfile object
    resp is of this format:
    {u'friends': {u'@attr': {u'for': u'havok07',
                         u'page': u'1',
                         u'perPage': u'50',
                         u'total': u'22',
                         u'totalPages': u'1'},
              u'user': [{u'image': [{u'#text': u'http://userserve-ak.last.fm/serve/34/57061383.jpg',
                                     u'size': u'small'},
                                    {u'#text': u'http://userserve-ak.last.fm/serve/64/57061383.jpg',
                                     u'size': u'medium'},
                                    {u'#text': u'http://userserve-ak.last.fm/serve/126/57061383.jpg',
                                     u'size': u'large'},
                                    {u'#text': u'http://userserve-ak.last.fm/serve/252/57061383.jpg',
                                     u'size': u'extralarge'}],
                         u'name': u'Lauren_Jaye',
                         u'realname': u'Lauren Miller',
                         u'url': u'http://www.last.fm/user/Lauren_Jaye'},
                        {u'image': [{u'#text': u'', u'size': u'small'},
                                    {u'#text': u'', u'size': u'medium'},
                                    {u'#text': u'', u'size': u'large'},
                                    {u'#text': u'', u'size': u'extralarge'}],
                         u'name': u'sysm',
                         u'realname': u'',
                         u'url': u'http://www.last.fm/user/sysm'}
                        ]}}'''
    for friend_data in resp.get('friends').get('user'):
        try:
            friend = UserProfile.objects.get(lfm_username=friend_data.get('name'))
        except ObjectDoesNotExist:
            friend = UserProfile(lfm_username=friend_data.get('name'))
            friend.url = friend_data.get('url')
            friend.name = friend_data.get('realname')
            
            image = None
            if friend_data.get('image')[0].get('#text'):
                image = Image(url=friend_data.get('image')[0].get('#text'))
            
            friend.image = image
            friend.save()
            
            get_for_user(friend.lfm_username)
        user.friends.add(friend)
        
    if resp.get('friends').get('@attr').get('totalPages') == resp.get('friends').get('@attr').get('page'):
        get_friends_data(user)
    
def get_friends_page(user, page=1):
    print 'getting friends page for %s'%user
    '''user is a UserProfile object'''
    url = get_friends_url(user.lfm_username, page=page)
    resp = do_call(url)
    total_pages = int(resp.get('friends').get('@attr').get('totalPages'))
    if page == 1:
        for page in range(2,total_pages+1):
            pass
            # job_data = {'uname':user.lfm_username, 'page':page}
            #             CLIENT.call('lfm.process_friends_page', json.dumps(job_data))
    process_friend_page(user, resp)
    
def process_track_info(resp):
    '''{u'track': {u'album': {u'@attr': {u'position': u'10'},
                           u'artist': u'deadmau5',
                           u'image': [{u'#text': u'http://userserve-ak.last.fm/serve/64s/39945013.jpg',
                                       u'size': u'small'},
                                      {u'#text': u'http://userserve-ak.last.fm/serve/126/39945013.jpg',
                                       u'size': u'medium'},
                                      {u'#text': u'http://userserve-ak.last.fm/serve/174s/39945013.jpg',
                                       u'size': u'large'},
                                      {u'#text': u'http://userserve-ak.last.fm/serve/300x300/39945013.jpg',
                                       u'size': u'extralarge'}],
                           u'mbid': u'4b1b7059-a511-4257-8fae-380eb36d36cd',
                           u'title': u'For Lack Of A Better Name',
                           u'url': u'http://www.last.fm/music/deadmau5/For+Lack+Of+A+Better+Name'},
                u'artist': {u'mbid': u'',
                            u'name': u'deadmau5',
                            u'url': u'http://www.last.fm/music/deadmau5'},
                u'duration': u'307000',
                u'id': u'332264316',
                u'listeners': u'68667',
                u'mbid': u'',
                u'name': u'Strobe',
                u'playcount': u'458109',
                u'streamable': {u'#text': u'0', u'fulltrack': u'0'},
                u'toptags': {u'tag': [{u'name': u'progressive house',
                                       u'url': u'http://www.last.fm/tag/progressive%20house'},
                                      {u'name': u'house',
                                       u'url': u'http://www.last.fm/tag/house'},
                                      {u'name': u'electronic',
                                       u'url': u'http://www.last.fm/tag/electronic'},
                                      {u'name': u'epic',
                                       u'url': u'http://www.last.fm/tag/epic'},
                                      {u'name': u'beautiful',
                                       u'url': u'http://www.last.fm/tag/beautiful'}]},
                u'url': u'http://www.last.fm/music/deadmau5/_/Strobe'}}'''
    track_dict = resp.get('track')
    try:
        track = Track.objects.get(name=track_dict.get('name'), artist__name=track_dict.get('artist').get('name'))
    except ObjectDoesNotExist:
        track = Track(name=track_dict.get('name'))
        
    track.album = None
    track.lfmid = track_dict.get('id')
    track.duration = int(track_dict.get('duration'))
    
    #image = Image(url=track_dict.get('album')[0].get('#text'))
    #image.save()
    #track.image = image
    
    track.name = track_dict.get('name')
    #TODO: track.tags
    #track.tag_count = 0
    track.url = track_dict.get('url')
    track.mbid = track_dict.get('mbid')
    track.listeners = track_dict.get('listeners')
    track.global_playcount = int(track_dict.get('playcount'))
    
    artist = get_or_create_artist(track_dict.get('artist').get('name'))

    track.artist = artist
    
    track.save()
        
def get_track_infos(track, artist):
    '''track and artist are strings.'''
    url = get_track_info_url(track, artist)
    resp = do_call(url)
    return resp
    

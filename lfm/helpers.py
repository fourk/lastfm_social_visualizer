import simplejson as json
import urllib2

from django.conf import settings



class Api(object):
    def __init__(self):
        self.API = settings.API
        
    def do_call(self, url):
        print '%s'%url
        return json.loads(urllib2.urlopen(url).read())

    def track_getinfo(self, track, artist):
        '''track and artist are strings'''
        url = 'http://ws.audioscrobbler.com/2.0/?method=track.getinfo&api_key=%s&track=%s&artist=%s&format=json'%(self.API, urllib2.quote(track.encode('utf-8')), urllib2.quote(artist.encode('utf-8')))
        return self.do_call(url)

    def user_get_toptracks_week(self, username, page=1):
        url = 'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&period=7day&api_key=%s&user=%s&format=json&page=%s'%(self.API, username, page)
        return self.do_call(url)

    def library_gettracks(self, username, page=1):
        #library.gettracks
        url = 'http://ws.audioscrobbler.com/2.0/?method=library.gettracks&api_key=%s&user=%s&format=json&page=%s'%(self.API, username, page)
        return self.do_call(url)

    def user_getfriends(self, username, page=1):
        #user.getfriends
        url = 'http://ws.audioscrobbler.com/2.0/?method=user.getfriends&api_key=%s&user=%s&format=json&page=%s'%(self.API, username, page)
        return self.do_call(url)

    def artist_getinfo(self, artist_name):
        url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&api_key=%s&artist=%s&format=json'%(self.API, urllib2.quote(artist_name.encode('utf-8')))
        return self.do_call(url)
    
    def user_getinfo(self, username):
        url =  'http://ws.audioscrobbler.com/2.0/?method=user.getinfo&api_key=%s&user=%s&format=json'%(self.API, username)
        return self.do_call(url)

    # def get_page(username, page=1, week=False):
    #     print 'PAGENUMBER',page
    #     if week:
    #         url = get_week_url(username, page)
    #     else:
    #         url = get_url(username, page)
    # 
    #     reply = urllib2.urlopen(url)
    #     return json.loads(reply.read())

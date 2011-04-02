# Create your views here.
from django.core.exceptions import ObjectDoesNotExist 
from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import operator
from lfm.models import UserProfile

try:
	import json
except ImportError:
	import simplejson as json
from django.template.context import RequestContext
from django.template.loader import get_template


def foo(request):
    username = request.GET.get('user')
    resp = helper(username)
    render(request, 'lfm/top100.html')
    
def helper(username, friends=True):
    cached = cache.get('dicks')
    if cached is not None:
        return cached
    try:
        user = UserProfile.objects.get(lfm_username=username)
        
    except ObjectDoesNotExist:
        return {'error': 'fuck, man.'}
        #TODO: handle this.
    listens = []
    if friends:
        [listens.append(listen) for friend in user.friends.all() for listen in friend.usertrackweek_set.all()]
    else:
        listens.append(user.usertrackweek_set.all())
        
    tracks = [listen.track for listen in listens]
    artists = set([track.artist for track in tracks])
    hash = {}
    if artists is None:
        return []
            
    for artist in artists:
        if artist:
            hash[artist.name] = {'sum_duration': 0,
                    'tracks': [],
                    'listens': [],
                    'artist_name': artist.name,
                    'listeners': [],
                    }
        
    for listen in listens:
        if listen.track.artist:
            hash[listen.track.artist.name]['listens'].append(listen)
            hash[listen.track.artist.name]['sum_duration'] += listen.track.duration/1000 * listen.personal_playcount
        
    # for track in tracks:
    #     hash[track.artist.name]['tracks'].append(track)
    #     hash[track.artist.name]['sum_duration'] += track.duration
    
    ls = []
    for k in hash:
        listeners = set([listen.user_profile for listen in hash[k].get('listens')])
        for listener in listeners:
            user_listens = [listen for listen in hash[k].get('listens') if listen.user_profile == listener]
            hash[k]['listeners'].append({
                    'user': listener,
                    'listens': user_listens,
                    'listening_duration': sum([listen.track.duration for listen in user_listens])/1000
                    })
        hash[k]['listeners'].sort(key=lambda x:x.get('listening_duration'), reverse=True)
        ls.append(hash[k])

    ls.sort(key=operator.itemgetter('sum_duration'), reverse=True)
    cache.set('dicks', ls, 60*60*2)
    return ls

def helper2(username):
    try:
        user = UserProfile.objects.get(lfm_username=username)
        
    except ObjectDoesNotExist:
        return {'error': 'fuck, man.'}
        #TODO: handle this.
    ls = []
    for friend in user.friends.all():
        ls.append({'user':friend, 'data':helper(friend.lfm_username)})
        
    return ls
    
# Create your views here.
from django.core.exceptions import ObjectDoesNotExist 
from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.cache import cache_page
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
    
def helper(username):
    try:
        user = UserProfile.objects.get(lfm_username=username)
        
    except ObjectDoesNotExist:
        return {'error': 'fuck, man.'}
        #TODO: handle this.
    
    listens = user.usertrackweek_set.all()
    tracks = [listen.track for listen in listens]
    artists = set([track.artist for track in tracks])
    hash = {}
    
    for artist in artists:
        hash[artist.name] = {'sum_duration':0,
                    'tracks':[],
                    'listens':[],
                    'artist_name':artist.name,
                    }
        
    for listen in listens:
        hash[listen.track.artist.name]['listens'].append(listen)
        hash[listen.track.artist.name]['sum_duration'] += listen.track.duration/1000 * listen.personal_playcount
        
    # for track in tracks:
    #     hash[track.artist.name]['tracks'].append(track)
    #     hash[track.artist.name]['sum_duration'] += track.duration
        
    ls = []
    for k in hash:
        ls.append(hash[k])

    ls.sort(key=operator.itemgetter('sum_duration'), reverse=True)
    
    for val in ls:
        val['sum_duration'] = "%s Seconds"%val['sum_duration']
    return ls
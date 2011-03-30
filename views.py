# Create your views here.
from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
#from rb.models import UserProfile,Track,UserArtist
#from rb.get_lfm_data import get_for_user
from django.conf import settings
from django.views.decorators.cache import cache_page
#from rb.update_dlc import get_all
import operator

try:
	import json
except ImportError:
	import simplejson as json
from django.template.context import RequestContext
from django.template.loader import get_template

# def home(request):
#   return render_to_response('index.html')
#   t = get_template('index.html')
#   html=t#.render()
#   return HttpResponse(html)
#   
# def user_page(request):
# # t=get_template('ajax.html')
# # return render_to_response('ajax.html')
# # return HttpResponse(t,mimetype='text/html')
#   try:
#       if len(Track.objects.all()) == 0:
#           get_all()
#       username = request.GET.get('lfmusername')
#       (profile,created) = UserProfile.objects.get_or_create(lfmusername=username)
#       if not profile.processed:
#           get_for_user(username)
#       try:
#           if profile.pages_loaded.count('1') == len(profile.pages_loaded):
#               progress_str = 'Thanks for using lastrbfm!'
#           else:
#               progress_str = '%s of %s pages of results processed... Reload the page in a few minutes for more results.'\
#                   %(profile.pages_loaded.count('1'),len(profile.pages_loaded))
#       except Exception:
#           progress_str = "Results 5% processed. Please wait a few moments and reload the page for full results. It can take up to a minute to retrieve all your artists from last.fm"
#       
#       artists = list(profile.artists.all())
#       tracks = Track.objects.filter(artist__in=artists).select_related('artist').order_by('artist__name')
#       tracks_out = []
#       [tracks_out.append({'artist':track.artist.name,'title':track.name}) for track in tracks]
#       
#       artists2 = list(set([track.artist for track in tracks]))
#       
#       relations = UserArtist.objects.filter(useraccount=profile,artist__in=artists2).all()
#       ht = {}
#       for relation in relations:
#           ht[relation.artist] = relation.listens
#       
#       
#       data_out = {}
#       data_out['music'] = []
#       for artist in artists2:
#           data_out['music'].append({'name':artist.name,'tracks':[track for track in tracks if track.artist==artist],'listens':int(ht[artist])})
# #     for artist in range(len(data_out['music'])):
# #         data_out['music'][artist]['tracks'] = [{'title':t.name,
# #                                             'cover':t.cover,
# #                                             'source':t.source,
# #                                             'genre':t.genre_symbol,
# #                                             'difficulty_band':t.difficulty_band,
# #                                             'difficulty_bass':t.difficulty_bass,
# #                                             'difficulty_guitar':t.difficulty_guitar,
# #                                             'difficulty_keys':t.difficulty_keys,
# #                                             'difficulty_vocals':t.difficulty_vocals,
# #                                             'difficulty_drums':t.difficulty_drums,
# #                                             } for t in data_out['music'][artist]['tracks']]
#           
# #     for track in tracks:
# #         if data_out.get(track.artist.name):
# #             data_out[track.artist.name]['tracks'].append({'title':track.name})
# #         else:
# #             data_out[track.artist.name]['tracks'] = [{'title':track.name}]
# #     for i in range(len(data_out['music'])):
# #         data_out['music'][i]['listens'] = 
#           
#       data_out['username'] = username
#       data_out['progress'] = progress_str
#       data_out['music'].sort(key=operator.itemgetter('listens'),reverse=True)
#   except Exception, e:
#       if settings.DEBUG:
#           raise
#       f=open(settings.LOG_DIRECTORY+"viewlog","a")
#       f.write(str(e)+'\n')
#       f.close()
#       
#   return render_to_response('ajax.html',data_out)
#   return HttpResponse(json.dumps(data_out),mimetype='application/javascript')
# # artists = [track.artist.name for track in tracks]
# # for 
def index(request):
    return render(request, 'login.html')
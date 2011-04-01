'''
Created on Dec 5, 2010

@author: jburkhart
'''
from django_beanstalkd import beanstalk_job
from lfm.data_proc import process_page, get_page, get_friends_page, process_friend_page, get_track_infos, process_track_info
from lfm.models import UserProfile, Track
import urllib2

try:
    import json
except ImportError:
    import simplejson as json
    
@beanstalk_job
def process_track_page(in_str):
    '''in_str will be a json serialized object of the following format
    {
        'uname':string,
        'page':int,
        'week':bool
    }
    '''
    data = json.loads(in_str)
    uname = data.get('uname')
    page = data.get('page')
    week = data.get('week')
    print 'processing %s'%page
    resp = get_page(uname, page=page, week=week)
    user = UserProfile.objects.get(lfm_username=uname)
    process_page(user, resp, week=week)

@beanstalk_job
def process_tags_for_track(in_str):
    '''in_str is json serialized object
    {
        'track_id':int
    }
    '''
    data = json.loads(in_str)
    track_id = data.get('track_id')
    track = Track.objects.get(track_id)
    pass
    
@beanstalk_job
def process_friends_page(in_str):
    '''
    in_str is a json serialized object of the following format:
    {
        'uname':string,
        'page':int
    }
    '''
    data = json.loads(in_str)
    uname = data.get('uname')
    page = data.get('page')
    resp = get_friends_page(uname, page)
    user = UserProfile.objects.get(lfm_username=uname)
    process_friend_page(user, resp)
    
# @beanstalk_job
# def get_friends_data(in_str):
#   pass

@beanstalk_job
def get_track_info(in_str):
    '''
    in_str is a json serialized object of the following format:
    {
        'track_name':string,
        'artist_name':string
    }
    '''
    data = json.loads(in_str)
    track_name = data.get('track_name')
    artist_name = data.get('artist_name')
    resp = get_track_infos(track_name, artist_name)
    process_track_info(resp)
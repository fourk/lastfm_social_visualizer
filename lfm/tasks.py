'''
Created on Dec 5, 2010

@author: jburkhart
'''
from celery.task import task
#from lfm.data_proc import process_page, get_page, get_friends_page, process_friend_page, get_track_infos, process_track_info, get_for_user
from lfm.models import UserProfile, Track
from django.db import reset_queries, close_connection
import urllib2
import datetime
from lfm.helpers import Api

Api = Api()
try:
    import json
except ImportError:
    import simplejson as json

@task
def userprofile_getinfo_task(id, nothing):
    userprofile = UserProfile.objects.get(id=id)
    userprofile._get_addtl_info()

@task
def track_getinfo_task(id, nothing):
    track = Track.objects.get(id=id)
    track._get_addtl_info()

@task
def update_trackweek_task(id, page=1):
    user = UserProfile.objects.get(id=id)
    user._update_trackweek(page=page)
 
@task   
def update_friends_task(id, page=1):
    user = UserProfile.objects.get(id=id)
    user._update_friends(page=page)
    
#######################################################################################################################
#
#                                                       OLD SHIT
#
#######################################################################################################################
# @task
# def process_track_page(in_str):
#     '''in_str will be a json serialized object of the following format
#     {
#         'uname':string,
#         'page':int,
#         'week':bool
#     }
#     '''
#     data = json.loads(in_str)
#     uname = data.get('uname')
#     page = data.get('page')
#     week = data.get('week')
#     print 'processing %s'%page
#     resp = get_page(uname, page=page, week=week)
#     user = UserProfile.objects.get(lfm_username=uname)
#     process_page(user, resp, week=week)
# 
# @task
# def process_tags_for_track(in_str):
#     '''in_str is json serialized object
#     {
#         'track_id':int
#     }
#     '''
#     data = json.loads(in_str)
#     track_id = data.get('track_id')
#     track = Track.objects.get(track_id)
#     pass
#     
# @task
# def process_friends_page(in_str):
#     '''
#     in_str is a json serialized object of the following format:
#     {
#         'uname':string,
#         'page':int
#     }
#     '''
#     data = json.loads(in_str)
#     uname = data.get('uname')
#     page = data.get('page')
#     resp = get_friends_page(uname, page)
#     user = UserProfile.objects.get(lfm_username=uname)
#     process_friend_page(user, resp)
#     
# # @task
# # def get_friends_data(in_str):
# #   pass
# @task
# def process_single_user(in_str):
#     pass
#     
# @task
# def process_all_friends(in_str):
#     pass
#     
# @task
# def get_track_info(in_str):
#     '''
#     in_str is a json serialized object of the following format:
#     {
#         'track_name':string,
#         'artist_name':string
#     }
#     '''
#     data = json.loads(in_str)
#     track_name = data.get('track_name')
#     artist_name = data.get('artist_name')
#     resp = get_track_infos(track_name, artist_name)
#     process_track_info(resp)
#     
# @task
# def get_user_track_week(in_str):
#     '''
#     in_str is a json serialized object of the following format:
#     {
#         'username':string
#     }
#     '''
#     data = json.loads(in_str)
#     username = data.get('username')
#     reset_queries()
#     close_connection()
#     user = UserProfile.objects.get(lfm_username=username)
#     if user.updating_track_week == True:
#         print 'Already updating get_user_track_week'
#         return
#     elif datetime.datetime.now() - user.tracks_week_updated_at < datetime.timedelta(7):
#         print 'Updated this user too recently'
#         return
#         
#     user.updating_track_week = True
#     user.save()
#     get_for_user(username, week=True)

@task
def add(x,y):
    return x+y


# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserTrackWeek'
        db.create_table('lfm_usertrackweek', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lfm.UserProfile'])),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lfm.Track'])),
            ('personal_playcount', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
        ))
        db.send_create_signal('lfm', ['UserTrackWeek'])

        # Changing field 'Image.url'
        db.alter_column('lfm_image', 'url', self.gf('django.db.models.fields.URLField')(max_length=254))


    def backwards(self, orm):
        
        # Deleting model 'UserTrackWeek'
        db.delete_table('lfm_usertrackweek')

        # Changing field 'Image.url'
        db.alter_column('lfm_image', 'url', self.gf('django.db.models.fields.URLField')(max_length=200))


    models = {
        'lfm.album': {
            'Meta': {'object_name': 'Album'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'albums'", 'to': "orm['lfm.Artist']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'global_playcount': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Image']", 'symmetrical': 'False'}),
            'lfmid': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'listeners': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tag_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Tag']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        'lfm.artist': {
            'Meta': {'object_name': 'Artist'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'global_playcount': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lfm.Image']", 'null': 'True', 'blank': 'True'}),
            'listeners': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'similar': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Artist']", 'through': "orm['lfm.SimilarArtist']", 'symmetrical': 'False'}),
            'tag_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Tag']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        'lfm.image': {
            'Meta': {'object_name': 'Image'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '254'})
        },
        'lfm.similarartist': {
            'Meta': {'object_name': 'SimilarArtist'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'similar_to'", 'to': "orm['lfm.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.FloatField', [], {}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'to_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'similar_from'", 'to': "orm['lfm.Artist']"})
        },
        'lfm.similartrack': {
            'Meta': {'object_name': 'SimilarTrack'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'similar_to'", 'to': "orm['lfm.Track']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.FloatField', [], {}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'to_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'similar_from'", 'to': "orm['lfm.Track']"})
        },
        'lfm.tag': {
            'Meta': {'object_name': 'Tag'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'reach': ('django.db.models.fields.IntegerField', [], {}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lfm.track': {
            'Meta': {'object_name': 'Track'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tracks'", 'null': 'True', 'to': "orm['lfm.Album']"}),
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tracks'", 'null': 'True', 'to': "orm['lfm.Artist']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '10'}),
            'global_playcount': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tracks'", 'null': 'True', 'to': "orm['lfm.Image']"}),
            'lfmid': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'listeners': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'similar': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Track']", 'through': "orm['lfm.SimilarTrack']", 'symmetrical': 'False'}),
            'tag_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Tag']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        'lfm.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.UserProfile']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lfm_username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'track_pages_loaded': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'tracks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lfm.Track']", 'through': "orm['lfm.UserTrack']", 'symmetrical': 'False'}),
            'tracks_week': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'userprofile_week_set'", 'symmetrical': 'False', 'through': "orm['lfm.UserTrackWeek']", 'to': "orm['lfm.Track']"})
        },
        'lfm.usertrack': {
            'Meta': {'object_name': 'UserTrack'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'personal_playcount': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lfm.Track']"}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lfm.UserProfile']"})
        },
        'lfm.usertrackweek': {
            'Meta': {'object_name': 'UserTrackWeek'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'personal_playcount': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lfm.Track']"}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lfm.UserProfile']"})
        }
    }

    complete_apps = ['lfm']

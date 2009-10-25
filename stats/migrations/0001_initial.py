
from south.db import db
from django.db import models
from muaccounts.models import *
from tracker.models import *
from stats.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'PackStatistics'
        db.create_table('stats_packstatistics', (
            ('basestatistics_ptr', orm['stats.PackStatistics:basestatistics_ptr']),
            ('pack', orm['stats.PackStatistics:pack']),
            ('trackerstats', orm['stats.PackStatistics:trackerstats']),
        ))
        db.send_create_signal('stats', ['PackStatistics'])
        
        # Adding model 'BaseStatistics'
        db.create_table('stats_basestatistics', (
            ('id', orm['stats.BaseStatistics:id']),
            ('created_date', orm['stats.BaseStatistics:created_date']),
        ))
        db.send_create_signal('stats', ['BaseStatistics'])
        
        # Adding model 'Statistics'
        db.create_table('stats_statistics', (
            ('id', orm['stats.Statistics:id']),
            ('owner', orm['stats.Statistics:owner']),
            ('interval', orm['stats.Statistics:interval']),
            ('daily_change', orm['stats.Statistics:daily_change']),
            ('total_24hours', orm['stats.Statistics:total_24hours']),
            ('total_7days', orm['stats.Statistics:total_7days']),
            ('daily_average', orm['stats.Statistics:daily_average']),
            ('most_active_source', orm['stats.Statistics:most_active_source']),
        ))
        db.send_create_signal('stats', ['Statistics'])
        
        # Adding model 'TrackerStatistics'
        db.create_table('stats_trackerstatistics', (
            ('basestatistics_ptr', orm['stats.TrackerStatistics:basestatistics_ptr']),
            ('tracker', orm['stats.TrackerStatistics:tracker']),
            ('trendstats', orm['stats.TrackerStatistics:trendstats']),
        ))
        db.send_create_signal('stats', ['TrackerStatistics'])
        
        # Adding model 'ChannelStatistics'
        db.create_table('stats_channelstatistics', (
            ('basestatistics_ptr', orm['stats.ChannelStatistics:basestatistics_ptr']),
            ('channel', orm['stats.ChannelStatistics:channel']),
            ('packstats', orm['stats.ChannelStatistics:packstats']),
        ))
        db.send_create_signal('stats', ['ChannelStatistics'])
        
        # Adding model 'TrendStatistics'
        db.create_table('stats_trendstatistics', (
            ('basestatistics_ptr', orm['stats.TrendStatistics:basestatistics_ptr']),
            ('trend', orm['stats.TrendStatistics:trend']),
        ))
        db.send_create_signal('stats', ['TrendStatistics'])
        
        # Creating unique_together for [pack, trackerstats] on PackStatistics.
        db.create_unique('stats_packstatistics', ['pack_id', 'trackerstats_id'])
        
        # Creating unique_together for [tracker, trendstats] on TrackerStatistics.
        db.create_unique('stats_trackerstatistics', ['tracker_id', 'trendstats_id'])
        
        # Creating unique_together for [channel, packstats] on ChannelStatistics.
        db.create_unique('stats_channelstatistics', ['channel_id', 'packstats_id'])
        
        # Creating unique_together for [owner, interval] on Statistics.
        db.create_unique('stats_statistics', ['owner_id', 'interval'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'PackStatistics'
        db.delete_table('stats_packstatistics')
        
        # Deleting model 'BaseStatistics'
        db.delete_table('stats_basestatistics')
        
        # Deleting model 'Statistics'
        db.delete_table('stats_statistics')
        
        # Deleting model 'TrackerStatistics'
        db.delete_table('stats_trackerstatistics')
        
        # Deleting model 'ChannelStatistics'
        db.delete_table('stats_channelstatistics')
        
        # Deleting model 'TrendStatistics'
        db.delete_table('stats_trendstatistics')
        
        # Deleting unique_together for [pack, trackerstats] on PackStatistics.
        db.delete_unique('stats_packstatistics', ['pack_id', 'trackerstats_id'])
        
        # Deleting unique_together for [tracker, trendstats] on TrackerStatistics.
        db.delete_unique('stats_trackerstatistics', ['tracker_id', 'trendstats_id'])
        
        # Deleting unique_together for [channel, packstats] on ChannelStatistics.
        db.delete_unique('stats_channelstatistics', ['channel_id', 'packstats_id'])
        
        # Deleting unique_together for [owner, interval] on Statistics.
        db.delete_unique('stats_statistics', ['owner_id', 'interval'])
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'muaccounts.muaccount': {
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '256', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'logo': ('RemovableImageField', [], {'null': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'owner': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'max_length': '256', 'unique': 'True', 'null': 'True'}),
            'theme': ('PickledObjectField', [], {'default': '( lambda :DEFAULT_THEME_DICT)'})
        },
        'stats.basestatistics': {
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'stats.channelstatistics': {
            'Meta': {'unique_together': "(('channel', 'packstats'),)"},
            'basestatistics_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['stats.BaseStatistics']", 'unique': 'True', 'primary_key': 'True'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['tracker.Channel']"}),
            'packstats': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'channelstats'", 'to': "orm['stats.PackStatistics']"})
        },
        'stats.packstatistics': {
            'Meta': {'unique_together': "(('pack', 'trackerstats'),)"},
            'basestatistics_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['stats.BaseStatistics']", 'unique': 'True', 'primary_key': 'True'}),
            'pack': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['tracker.Pack']"}),
            'trackerstats': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'packstats'", 'to': "orm['stats.TrackerStatistics']"})
        },
        'stats.statistics': {
            'Meta': {'unique_together': "(('owner', 'interval'),)"},
            'daily_average': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'daily_change': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'most_active_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['stats.BaseStatistics']"}),
            'total_24hours': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_7days': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'stats.trackerstatistics': {
            'Meta': {'unique_together': "(('tracker', 'trendstats'),)"},
            'basestatistics_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['stats.BaseStatistics']", 'unique': 'True', 'primary_key': 'True'}),
            'tracker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['tracker.Tracker']"}),
            'trendstats': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trackerstats'", 'to': "orm['stats.TrendStatistics']"})
        },
        'stats.trendstatistics': {
            'basestatistics_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['stats.BaseStatistics']", 'unique': 'True', 'primary_key': 'True'}),
            'trend': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tracker.Trend']", 'unique': 'True'})
        },
        'tracker.channel': {
            'api': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'})
        },
        'tracker.pack': {
            'channels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tracker.Channel']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'muaccounts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['muaccounts.MUAccount']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'})
        },
        'tracker.tracker': {
            'counter': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'en-US'", 'max_length': '5'}),
            'laststarted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'muaccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trackers'", 'to': "orm['muaccounts.MUAccount']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'packs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tracker.Pack']"}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'radius': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'startdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'})
        },
        'tracker.trend': {
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'muaccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trends'", 'to': "orm['muaccounts.MUAccount']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'trackers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tracker.Tracker']"})
        }
    }
    
    complete_apps = ['stats']

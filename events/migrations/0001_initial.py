# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'events_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('event_type', self.gf('django.db.models.fields.CharField')(default='public', max_length=255)),
            ('event_status', self.gf('django.db.models.fields.CharField')(default='active', max_length=255)),
            ('event_date', self.gf('django.db.models.fields.DateField')()),
            ('event_time', self.gf('django.db.models.fields.TimeField')()),
            ('event_create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('event_detail', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('event_view_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('event_capacity', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('event_recent_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('fk_event_poster_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['basal.CustomUser'])),
            ('address_detail', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_city', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address_region', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address_country', self.gf('django.db.models.fields.CharField')(default='Canada', max_length=255, blank=True)),
            ('address_postal_code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'events', ['Event'])

        # Adding model 'EventRSVP'
        db.create_table(u'events_eventrsvp', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fk_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['basal.CustomUser'])),
            ('fk_event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
        ))
        db.send_create_signal(u'events', ['EventRSVP'])

        # Adding model 'EventLike'
        db.create_table(u'events_eventlike', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fk_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['basal.CustomUser'])),
            ('fk_event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
        ))
        db.send_create_signal(u'events', ['EventLike'])

        # Adding model 'EventComment'
        db.create_table(u'events_eventcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment_detail', self.gf('django.db.models.fields.TextField')()),
            ('comment_post_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fk_event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_comment', to=orm['events.Event'])),
            ('fk_comment_poster_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['basal.CustomUser'])),
        ))
        db.send_create_signal(u'events', ['EventComment'])

        # Adding model 'Tag'
        db.create_table(u'events_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'events', ['Tag'])

        # Adding model 'TagEventAttribute'
        db.create_table(u'events_tageventattribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fk_tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Tag'])),
            ('fk_event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
        ))
        db.send_create_signal(u'events', ['TagEventAttribute'])

        # Adding model 'EventImage'
        db.create_table(u'events_eventimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('fk_event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_image', to=orm['events.Event'])),
        ))
        db.send_create_signal(u'events', ['EventImage'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'events_event')

        # Deleting model 'EventRSVP'
        db.delete_table(u'events_eventrsvp')

        # Deleting model 'EventLike'
        db.delete_table(u'events_eventlike')

        # Deleting model 'EventComment'
        db.delete_table(u'events_eventcomment')

        # Deleting model 'Tag'
        db.delete_table(u'events_tag')

        # Deleting model 'TagEventAttribute'
        db.delete_table(u'events_tageventattribute')

        # Deleting model 'EventImage'
        db.delete_table(u'events_eventimage')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'basal.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'fk_user_background_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_background_image'", 'null': 'True', 'to': u"orm['basal.UserImage']"}),
            'fk_user_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_image'", 'null': 'True', 'to': u"orm['basal.UserImage']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user_first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user_gender': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user_last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user_location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user_nickname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'basal.userimage': {
            'Meta': {'object_name': 'UserImage'},
            'fk_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_image'", 'to': u"orm['basal.CustomUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_country': ('django.db.models.fields.CharField', [], {'default': "'Canada'", 'max_length': '255', 'blank': 'True'}),
            'address_detail': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'event_capacity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'event_create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_date': ('django.db.models.fields.DateField', [], {}),
            'event_detail': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_recent_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'event_status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '255'}),
            'event_time': ('django.db.models.fields.TimeField', [], {}),
            'event_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'event_type': ('django.db.models.fields.CharField', [], {'default': "'public'", 'max_length': '255'}),
            'event_view_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'fk_event_poster_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['basal.CustomUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'events.eventcomment': {
            'Meta': {'object_name': 'EventComment'},
            'comment_detail': ('django.db.models.fields.TextField', [], {}),
            'comment_post_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fk_comment_poster_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['basal.CustomUser']"}),
            'fk_event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_comment'", 'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'events.eventimage': {
            'Meta': {'object_name': 'EventImage'},
            'fk_event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_image'", 'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'events.eventlike': {
            'Meta': {'object_name': 'EventLike'},
            'fk_event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            'fk_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['basal.CustomUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'events.eventrsvp': {
            'Meta': {'object_name': 'EventRSVP'},
            'fk_event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            'fk_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['basal.CustomUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'events.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'events.tageventattribute': {
            'Meta': {'object_name': 'TagEventAttribute'},
            'fk_event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            'fk_tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Tag']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['events']
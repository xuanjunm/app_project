# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CustomUser'
        db.create_table(u'basal_customuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('user_first_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('user_last_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user_gender', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('user_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user_nickname', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('user_location', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('fk_user_background_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_background_image', null=True, to=orm['basal.UserImage'])),
            ('fk_user_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_image', null=True, to=orm['basal.UserImage'])),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'basal', ['CustomUser'])

        # Adding M2M table for field groups on 'CustomUser'
        m2m_table_name = db.shorten_name(u'basal_customuser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customuser', models.ForeignKey(orm[u'basal.customuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['customuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'CustomUser'
        m2m_table_name = db.shorten_name(u'basal_customuser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customuser', models.ForeignKey(orm[u'basal.customuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['customuser_id', 'permission_id'])

        # Adding model 'UserImage'
        db.create_table(u'basal_userimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('fk_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_image', to=orm['basal.CustomUser'])),
        ))
        db.send_create_signal(u'basal', ['UserImage'])

        # Adding model 'Address'
        db.create_table(u'basal_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fk_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='address', to=orm['basal.CustomUser'])),
            ('address_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_detail', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_city', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address_region', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address_country', self.gf('django.db.models.fields.CharField')(default='Canada', max_length=255, blank=True)),
            ('address_postal_code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'basal', ['Address'])

        # Adding model 'UserFriendAttribute'
        db.create_table(u'basal_userfriendattribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fk_friend_a_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friend_a', to=orm['basal.CustomUser'])),
            ('fk_friend_b_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friend_b', to=orm['basal.CustomUser'])),
        ))
        db.send_create_signal(u'basal', ['UserFriendAttribute'])

        # Adding model 'UserTag'
        db.create_table(u'basal_usertag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fk_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_tag', to=orm['basal.CustomUser'])),
        ))
        db.send_create_signal(u'basal', ['UserTag'])


    def backwards(self, orm):
        # Deleting model 'CustomUser'
        db.delete_table(u'basal_customuser')

        # Removing M2M table for field groups on 'CustomUser'
        db.delete_table(db.shorten_name(u'basal_customuser_groups'))

        # Removing M2M table for field user_permissions on 'CustomUser'
        db.delete_table(db.shorten_name(u'basal_customuser_user_permissions'))

        # Deleting model 'UserImage'
        db.delete_table(u'basal_userimage')

        # Deleting model 'Address'
        db.delete_table(u'basal_address')

        # Deleting model 'UserFriendAttribute'
        db.delete_table(u'basal_userfriendattribute')

        # Deleting model 'UserTag'
        db.delete_table(u'basal_usertag')


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
        u'basal.address': {
            'Meta': {'object_name': 'Address'},
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_country': ('django.db.models.fields.CharField', [], {'default': "'Canada'", 'max_length': '255', 'blank': 'True'}),
            'address_detail': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fk_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'address'", 'to': u"orm['basal.CustomUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        u'basal.userfriendattribute': {
            'Meta': {'object_name': 'UserFriendAttribute'},
            'fk_friend_a_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friend_a'", 'to': u"orm['basal.CustomUser']"}),
            'fk_friend_b_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friend_b'", 'to': u"orm['basal.CustomUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'basal.userimage': {
            'Meta': {'object_name': 'UserImage'},
            'fk_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_image'", 'to': u"orm['basal.CustomUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'basal.usertag': {
            'Meta': {'object_name': 'UserTag'},
            'fk_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_tag'", 'to': u"orm['basal.CustomUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['basal']
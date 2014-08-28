# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'State.codename'
        db.add_column(u'workflows_state', 'codename',
                      self.gf('django.db.models.fields.CharField')(default='codename', max_length=100),
                      keep_default=False)

        # Adding field 'State.description'
        db.add_column(u'workflows_state', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'State.state_position'
        db.add_column(u'workflows_state', 'state_position',
                      self.gf('django.db.models.fields.IntegerField')(default=-1, db_index=True),
                      keep_default=False)

        # Adding unique constraint on 'State', fields ['codename', 'workflow']
        db.create_unique(u'workflows_state', ['codename', 'workflow_id'])

        # Adding unique constraint on 'State', fields ['name', 'workflow']
        db.create_unique(u'workflows_state', ['name', 'workflow_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'State', fields ['name', 'workflow']
        db.delete_unique(u'workflows_state', ['name', 'workflow_id'])

        # Removing unique constraint on 'State', fields ['codename', 'workflow']
        db.delete_unique(u'workflows_state', ['codename', 'workflow_id'])

        # Deleting field 'State.codename'
        db.delete_column(u'workflows_state', 'codename')

        # Deleting field 'State.description'
        db.delete_column(u'workflows_state', 'description')

        # Deleting field 'State.state_position'
        db.delete_column(u'workflows_state', 'state_position')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'permissions.permission': {
            'Meta': {'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'content_types': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'content_types'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'permissions.role': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'workflows.state': {
            'Meta': {'ordering': "['state_position']", 'unique_together': "(('codename', 'workflow'), ('name', 'workflow'))", 'object_name': 'State'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'state_position': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'db_index': 'True'}),
            'transitions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'states'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['workflows.Transition']"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'states'", 'to': u"orm['workflows.Workflow']"})
        },
        u'workflows.stateinheritanceblock': {
            'Meta': {'object_name': 'StateInheritanceBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['permissions.Permission']"}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workflows.State']"})
        },
        u'workflows.stateobjectrelation': {
            'Meta': {'unique_together': "(('content_type', 'content_id', 'state'),)", 'object_name': 'StateObjectRelation'},
            'content_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'state_object'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workflows.State']"})
        },
        u'workflows.statepermissionrelation': {
            'Meta': {'object_name': 'StatePermissionRelation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['permissions.Permission']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['permissions.Role']"}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workflows.State']"})
        },
        u'workflows.transition': {
            'Meta': {'object_name': 'Transition'},
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'destination_state'", 'null': 'True', 'to': u"orm['workflows.State']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['permissions.Permission']", 'null': 'True', 'blank': 'True'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transitions'", 'to': u"orm['workflows.Workflow']"})
        },
        u'workflows.workflow': {
            'Meta': {'object_name': 'Workflow'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_state': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'workflow_state'", 'null': 'True', 'to': u"orm['workflows.State']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['permissions.Permission']", 'through': u"orm['workflows.WorkflowPermissionRelation']", 'symmetrical': 'False'})
        },
        u'workflows.workflowmodelrelation': {
            'Meta': {'object_name': 'WorkflowModelRelation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wmrs'", 'to': u"orm['workflows.Workflow']"})
        },
        u'workflows.workflowobjectrelation': {
            'Meta': {'unique_together': "(('content_type', 'content_id'),)", 'object_name': 'WorkflowObjectRelation'},
            'content_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'workflow_object'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wors'", 'to': u"orm['workflows.Workflow']"})
        },
        u'workflows.workflowpermissionrelation': {
            'Meta': {'unique_together': "(('workflow', 'permission'),)", 'object_name': 'WorkflowPermissionRelation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'permissions'", 'to': u"orm['permissions.Permission']"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workflows.Workflow']"})
        }
    }

    complete_apps = ['workflows']
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import positions.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('permissions', '__first__'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codename', models.CharField(max_length=100, verbose_name='Codename')),
                ('name', models.CharField(max_length=100, verbose_name='Name', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('state_position', positions.fields.PositionField(default=-1, db_index=True)),
            ],
            options={
                'ordering': ['state_position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StateInheritanceBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.ForeignKey(verbose_name='Permission', to='permissions.Permission')),
                ('state', models.ForeignKey(verbose_name='State', to='workflows.State')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StateObjectRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_id', models.PositiveIntegerField(null=True, verbose_name='Content id', blank=True)),
                ('content_type', models.ForeignKey(related_name='state_object', verbose_name='Content type', blank=True, to='contenttypes.ContentType', null=True)),
                ('state', models.ForeignKey(verbose_name='State', to='workflows.State')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatePermissionRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.ForeignKey(verbose_name='Permission', to='permissions.Permission')),
                ('role', models.ForeignKey(verbose_name='Role', to='permissions.Role')),
                ('state', models.ForeignKey(verbose_name='State', to='workflows.State')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name', blank=True)),
                ('direction', models.IntegerField(default=0, verbose_name='direction', choices=[(0, 'None'), (1, 'Forward'), (-1, 'Backward')])),
                ('condition', models.CharField(max_length=100, verbose_name='Condition', blank=True)),
                ('destination', models.ForeignKey(related_name='destination_state', verbose_name='Destination', blank=True, to='workflows.State', null=True)),
                ('permission', models.ForeignKey(verbose_name='Permission', blank=True, to='permissions.Permission', null=True)),
            ],
            options={
                'ordering': ['destination'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransitionObjectRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_id', models.PositiveIntegerField(null=True, verbose_name='Content id', blank=True)),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='datetime')),
                ('content_type', models.ForeignKey(related_name='transition_object', verbose_name='Content type', blank=True, to='contenttypes.ContentType', null=True)),
                ('state', models.ForeignKey(verbose_name='State', to='workflows.State')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-datetime', '-id'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('initial_state', models.ForeignKey(related_name='workflow_state', verbose_name='Initial state', blank=True, to='workflows.State', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkflowModelRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_type', models.ForeignKey(verbose_name='Content Type', to='contenttypes.ContentType', unique=True)),
                ('workflow', models.ForeignKey(related_name='wmrs', verbose_name='Workflow', to='workflows.Workflow')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkflowObjectRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_id', models.PositiveIntegerField(null=True, verbose_name='Content id', blank=True)),
                ('content_type', models.ForeignKey(related_name='workflow_object', verbose_name='Content type', blank=True, to='contenttypes.ContentType', null=True)),
                ('workflow', models.ForeignKey(related_name='wors', verbose_name='Workflow', to='workflows.Workflow')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkflowPermissionRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.ForeignKey(related_name='permissions', to='permissions.Permission')),
                ('workflow', models.ForeignKey(to='workflows.Workflow')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='workflowpermissionrelation',
            unique_together=set([('workflow', 'permission')]),
        ),
        migrations.AlterUniqueTogether(
            name='workflowobjectrelation',
            unique_together=set([('content_type', 'content_id')]),
        ),
        migrations.AddField(
            model_name='workflow',
            name='permissions',
            field=models.ManyToManyField(to='permissions.Permission', verbose_name='Permissions', through='workflows.WorkflowPermissionRelation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transition',
            name='workflow',
            field=models.ForeignKey(related_name='transitions', verbose_name='Workflow', to='workflows.Workflow'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='transition',
            unique_together=set([('destination', 'direction')]),
        ),
        migrations.AlterUniqueTogether(
            name='stateobjectrelation',
            unique_together=set([('content_type', 'content_id', 'state')]),
        ),
        migrations.AddField(
            model_name='state',
            name='transitions',
            field=models.ManyToManyField(related_name='states', null=True, verbose_name='Transitions', to='workflows.Transition', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='state',
            name='workflow',
            field=models.ForeignKey(related_name='states', verbose_name='Workflow', to='workflows.Workflow'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='state',
            unique_together=set([('codename', 'workflow'), ('name', 'workflow')]),
        ),
    ]

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from workflows.models import State
from workflows.models import StateInheritanceBlock
from workflows.models import StatePermissionRelation
from workflows.models import StateObjectRelation
from workflows.models import TransitionObjectRelation
from workflows.models import Transition
from workflows.models import Workflow
from workflows.models import WorkflowObjectRelation
from workflows.models import WorkflowModelRelation
from workflows.models import WorkflowPermissionRelation


def retrieve_object_id_from_path(request):
    #TODO: is there a better way ?
    # ex: u'/admin/paintdb/recipe/203421/'
    path_info = request.META['PATH_INFO']
    object_id = int(path_info.strip('/').split('/')[-1])
    return object_id


class StateAdmin(admin.ModelAdmin):
    list_display = ['codename', 'name', 'transition_listing', 'workflow', 'state_position', 'description', ]
    list_editable = ['state_position', 'description', ]
    list_filter = ['workflow', ]
    filter_horizontal = ['transitions', ]
    search_fields = ['codename', 'name', ]

    def transition_listing(self, obj):
        try:
            html = '<br />'.join([item.__unicode__() for item in obj.transitions.all()])
        except:
            html = ''
        return html
    transition_listing.short_description = _(u'transitions')
    transition_listing.allow_tags = True

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'transitions':
            try:
                state = State.objects.get(id=retrieve_object_id_from_path(request))
                queryset = state.workflow.transitions
            except:
                queryset = Transition.objects.all()
            kwargs["queryset"] = queryset
        return super(StateAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class StateInline(admin.StackedInline):
    model = State
    filter_horizontal = ['transitions', ]
    extra = 0

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'transitions':
            try:
                workflow = Workflow.objects.get(id=retrieve_object_id_from_path(request))
                queryset = workflow.transitions
            except:
                queryset = Transition.objects.all()
            kwargs["queryset"] = queryset
        return super(StateInline, self).formfield_for_manytomany(db_field, request, **kwargs)


class WorkflowAdmin(admin.ModelAdmin):
    inlines = [
        StateInline,
    ]
    list_display = ['name', 'initial_state', 'state_listing', 'transition_listing', ]

    def state_listing(self, obj):
        try:
            html = '<br />'.join([item.__unicode__() for item in obj.states.all()])
        except:
            html = ''
        return html
    state_listing.short_description = _(u'states')
    state_listing.allow_tags = True

    def transition_listing(self, obj):
        try:
            html = '<br />'.join([item.__unicode__() for item in obj.transitions.all()])
        except:
            html = ''
        return html
    transition_listing.short_description = _(u'transitions')
    transition_listing.allow_tags = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "initial_state":
            try:
                workflow = Workflow.objects.get(id=retrieve_object_id_from_path(request))
                queryset = workflow.states.all()
            except:
                queryset = State.objects.all()
            kwargs["queryset"] = queryset
        return super(WorkflowAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class TransitionAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'destination', 'direction', 'permission_listing', 'workflow', ]
    list_filter = ['workflow', ]

    def permission_listing(self, obj):
        try:
            html = '<br />'.join([item.__unicode__() for item in obj.permissions.all()])
        except:
            html = ''
        return html
    permission_listing.short_description = _(u'permissions')
    permission_listing.allow_tags = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'destination':
            try:
                transition = Transition.objects.get(id=retrieve_object_id_from_path(request))
                queryset = transition.workflow.states
            except:
                queryset = State.objects.all()
            kwargs["queryset"] = queryset
        return super(TransitionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class TransitionObjectRelationAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'content', 'state', 'user', ]
    date_hierarchy = 'datetime'
    search_fields = ['user__username', ]


class WorkflowModelRelationAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'content_type', 'workflow', ]
    list_filter = ['workflow', ]


class WorkflowPermissionRelationAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'workflow', 'permission', ]
    list_filter = ['workflow', ]


class StatePermissionRelationAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'state', 'permission', 'role', ]


class StateInheritanceBlockAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'state', 'permission', ]


admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(StateInheritanceBlock, StateInheritanceBlockAdmin)
admin.site.register(StateObjectRelation)
admin.site.register(StatePermissionRelation, StatePermissionRelationAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(WorkflowObjectRelation)
admin.site.register(WorkflowModelRelation, WorkflowModelRelationAdmin)
admin.site.register(WorkflowPermissionRelation, WorkflowPermissionRelationAdmin)
admin.site.register(TransitionObjectRelation, TransitionObjectRelationAdmin)

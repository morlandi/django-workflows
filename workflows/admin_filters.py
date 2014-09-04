from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from .utils import get_workflow_for_model


class WorkflowStatesFilter(admin.RelatedFieldListFilter):

    def __init__(self, field, request, params, model, model_admin, field_path):
        """
            Sample usage (in ModelAdmin):

            list_filter = [('state', WorkflowStatesFilter), ...
        """
        super(WorkflowStatesFilter, self).__init__(field, request, params, model, model_admin, field_path)
        # if a specific workflow is associated with this model,
        # filter state values accordingly
        try:
            ctype = ContentType.objects.get_for_model(model_admin.model)
            workflow = get_workflow_for_model(ctype)
            states = workflow.states.all()
            self.lookup_choices = states.values_list('id', 'name')
        except:
            pass

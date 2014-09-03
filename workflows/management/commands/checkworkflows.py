import os.path
from optparse import make_option
from django.db import DEFAULT_DB_ALIAS
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import CommandError
from django.core.management.base import BaseCommand
from workflows.models import Workflow
from workflows.models import State
from workflows.models import Transition
from workflows.models import WorkflowModelRelation
from .base import BaseWorkflowCommand


############################################################################################

class Command(BaseWorkflowCommand):
    args = '<fixture>'
    help = 'Compare fixture with installed workflows'

    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a specific database to load '
                'fixtures into. Defaults to the "default" database.'),
    )

    def handle(self, *args, **options):

        self.verbosity = int(options.get('verbosity'))
        using = options.get('database')

        # We normally to not use transactions for this command as not changes
        # to the db are required
        commit = options.get('commit', False)

        # Start transaction management. All fixtures are installed in a
        # single transaction to ensure that all references are resolved.
        if commit:
            transaction.commit_unless_managed(using=using)
            transaction.enter_transaction_management(using=using)
            transaction.managed(True, using=using)

        # check args
        if len(args) < 1:
            raise CommandError('No fixture specified')

        # check files
        fixture = args[0]

        try:
            self.work(fixture, using)
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception as e:
            if commit:
                transaction.rollback(using=using)
                transaction.leave_transaction_management(using=using)
            raise

        if commit:
            transaction.commit(using=using)
            transaction.leave_transaction_management(using=using)

    def work(self, fixture, using):

        if not os.path.isfile(fixture):
            raise CommandError('Fixture "%s" not found' % fixture)

        objects = self.deserialize_objects(fixture, using, self.verbosity)

        # If the fixture we loaded contains 0 objects, assume that an
        # error was encountered during fixture loading.
        if len(objects) == 0:
            raise CommandError("No fixture data found for '%s'. (File format may be invalid.)" % (fixture))

        errors = 0
        models = [Workflow, State, Transition, WorkflowModelRelation, ]
        #models = [State, ]
        for model in models:
            deserialized_objects = [obj for obj in objects if type(obj.object) is model]
            errors += self.check_objects(deserialized_objects, using)

        self.trace('\nTotal number of failed comparisons: %d\n\n' % errors, 1)

    def compare_objects(self, source_deserialized_obj, target_obj, m2m_accessors, using):
        """ Given source (from fixture) and target (from db) objects,
            compares every single attribute.
            Returns the number of discrepancies
        """
        errors = 0

        # Code adapted from Model.save_base()
        source_obj = source_deserialized_obj.object
        cls = source_obj.__class__
        meta = cls._meta
        cls_name = meta.object_name
        non_pks = [f for f in meta.local_fields if not f.primary_key]

        source_values = dict([(f.attname, getattr(source_obj, f.attname)) for f in non_pks])
        target_values = dict([(f.attname, getattr(target_obj, f.attname)) for f in non_pks])

        # compare single attributes
        for key, value in source_values.items():
            tvalue = target_values.get(key, None)
            message = '[%s:%d:%s]: source value = "%s", target value = "%s"' % (cls_name, source_obj.pk, key, unicode(value), unicode(tvalue))
            if self.verbosity >= 3:
                self.stdout.write(message)
            if value != tvalue:
                self.trace_error(message)
                errors = errors + 1

        # compare related objects
        for accessor in m2m_accessors:
            source_related_objects_ids = sorted([int(item) for item in source_deserialized_obj.m2m_data[accessor]])
            target_related_objects_ids = sorted(getattr(target_obj, accessor).all().values_list('pk', flat=True))
            message = '[%s:%d:%s]: source value = "%s", target value = "%s"' % (cls_name, source_obj.id, accessor, unicode(source_related_objects_ids), unicode(target_related_objects_ids))
            if self.verbosity >= 3:
                self.stdout.write(message)
            if cmp(source_related_objects_ids, target_related_objects_ids) != 0:
                self.trace_error(message)
                errors = errors + 1

        return errors

    def check_objects(self, deserialized_objects, using):
        """  Receives a list of objects deserialized from fixture (must be of the same type),
             retrieve the correstonding list of objects form database,
             then compares the two lists.
             Returns the number of discrepancies.
        """
        errors = 0

        if len(deserialized_objects) <= 0:
            self.trace_error('Empty deserialized objects list (warning)')
            return

        cls = deserialized_objects[0].object.__class__
        cls_name = cls._meta.object_name
        self.trace('*** %ss comparison (source=fixture, target=database)' % cls_name)

        db_objects = cls.objects.all()
        m2m_accessors = deserialized_objects[0].m2m_data.keys()

        # scan db objects
        fixture_objects_pks = [item.object.pk for item in deserialized_objects]
        for obj in db_objects:
            if obj.pk not in fixture_objects_pks:
                self.trace_error('%s [%d] present in database but missing from fixtures' % (cls_name, obj.pk))
                errors += 1

        # scan fixture objects
        for source_deserialized_obj in deserialized_objects:
            try:
                # compare every attribute of source and target objects
                target_obj = db_objects.get(pk=source_deserialized_obj.object.pk)
                errors += self.compare_objects(source_deserialized_obj, target_obj, m2m_accessors, using)
            except ObjectDoesNotExist:
                self.trace_error('%s [%d] present in fixtures but missing from database' % (cls_name, source_deserialized_obj.object.pk))
                errors += 1

        return errors

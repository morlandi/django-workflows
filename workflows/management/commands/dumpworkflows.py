from django.core.management.commands.dumpdata import Command as DumpdataCommand
from django.core.management.base import BaseCommand
from optparse import make_option
from django.db import DEFAULT_DB_ALIAS


class Command(DumpdataCommand):

    option_list = BaseCommand.option_list + (
        # make_option('--format', default='json', dest='format',
        #     help='Specifies the output serialization format for fixtures.'),
        # make_option('--indent', default=None, dest='indent', type='int',
        #     help='Specifies the indent level to use when pretty-printing output'),
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a specific database to dump '
                'fixtures from. Defaults to the "default" database.'),
        make_option('-e', '--exclude', dest='exclude', action='append', default=[],
            help='An appname or appname.ModelName to exclude (use multiple --exclude to exclude multiple apps/models).'),
        # make_option('-n', '--natural', action='store_true', dest='use_natural_keys', default=False,
        #     help='Use natural keys if they are available.'),
        make_option('-a', '--all', action='store_true', dest='use_base_manager', default=False,
            help="Use Django's base manager to dump all models stored in the database, including those that would otherwise be filtered or modified by a custom manager."),
    )
    help = ("Dumps a fixture of Workflows related tables; the output is suitable for 'checkworkflows' and 'loaddata' commands")
    args = ''

    def handle(self, *app_labels, **options):

        app_labels = (
            'workflows.Workflow',
            'workflows.State',
            'workflows.Transition',
            'workflows.WorkflowModelRelation'
        )

        options['format'] = 'json'
        options['indent'] = 2
        options['use_natural_keys'] = True

        super(Command, self).handle(*app_labels, **options)

from django.core import serializers
from django.core.management.base import CommandError
from django.core.management.base import BaseCommand


class BaseWorkflowCommand(BaseCommand):

    def deserialize_objects(self, fixture, database, verbosity):
        """ Adapted from 'loaddata' django command
            Returns a list of objects loaded from a single fixture;
            no comporession accepted at the moment
        """

        objects_list = []

        humanize = lambda dirname: "'%s'" % dirname if dirname else 'absolute path'
        parts = fixture.split('.')
        if len(parts) == 1:
            fixture_name = parts[0]
            formats = serializers.get_public_serializer_formats()
        else:
            fixture_name, format = '.'.join(parts[:-1]), parts[-1]
            if format in serializers.get_public_serializer_formats():
                formats = [format]
            else:
                formats = []

        if formats:
            if verbosity >= 2:
                self.stdout.write("Checking '%s' fixture..." % fixture_name)
        else:
            raise CommandError(
                "Problem deserializing fixture '%s': %s is not a known serialization format." %
                    (fixture_name, format))

        fixture_dir = fixture_name

        format = formats[0]
        full_path = '.'.join([fixture_dir, format])

        open_method = open
        try:
            fixture = open_method(full_path, 'r')
        except IOError:
            if verbosity >= 2:
                self.stdout.write("No %s fixture '%s' in %s." % (format, fixture_name, humanize(fixture_dir)))
        else:
            try:
                objects = serializers.deserialize(format, fixture, using=database, ignorenonexistent=False)
                for object in objects:
                    objects_list.append(object)

            except Exception as e:
                if not isinstance(e, CommandError):
                    e.args = ("Problem deserializing fixture '%s': %s" % (full_path, e),)
                raise
            finally:
                fixture.close()

        return objects_list

    def trace(self, message, min_verbosity=2):
        if self.verbosity >= min_verbosity:
            if type(message) is list:
                text = ' '.join(message)
            else:
                text = message
            self.stdout.write(text)

    def trace_error(self, message):
        self.trace(['\x1b[1;;43;30m', 'ERROR:', message, '\x1b[0m'], 1)

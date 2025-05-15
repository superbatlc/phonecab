from django.core.management.base import BaseCommand, CommandError
from helper.importer import Importer


class Command(BaseCommand):
    help = 'Handle import of Persons and Whitelists'

    def add_arguments(self, parser):

        parser.add_argument(
            '--phoneusers',
            action='store_true',
            help='Import main info and language of the Phoneusers'
        )

        parser.add_argument(
            '--whitelists',
            action='store_true',
            help='Import whitelists of the Phoneusers'

        )

        parser.add_argument(
            '--filename',
            action='store_true',
            help='Path to CSV file for import'
        )


    def handle(self, *args, **options):

        filename = options['filename']
        if not filename or filename == '':
            self.stderr.write('Missing filename')

        if options['phoneusers']:
            Importer.import_phoneusers(filename=filename)
        if options['whitelists']:
            Importer.import_whitelist(filename=filename)

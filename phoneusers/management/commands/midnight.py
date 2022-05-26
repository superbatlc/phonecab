from django.core.management.base import BaseCommand, CommandError
from phoneusers.models import PhoneUser, Whitelist


class Command(BaseCommand):
    help = 'Disable cards and permissions'

    debug = False

    def add_arguments(self, parser):
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Print debug information'
        )

        parser.add_argument(
            '--disable-cards',
            action='store_true',
            help='Disable all the cards'
        )

        parser.add_argument(
            '--disable-whitelists',
            action='store_true',
            help='Disable all the whitelists'
        )

        parser.add_argument(
            '--disable-extraordinary',
            action='store_true',
            help='Disable all the extraordinary permissions'
        )

        parser.add_argument(
            '--disable-all',
            action='store_true',
            help='Disable cards, whitelists and disable extraordinary permissions'
        )

    def handle(self, *args, **options):

        self.debug = options['debug']

        if options['disable_all']:

            self.disable_cards()
            self.disable_whitelists()
            self.disable_extraordinary()
        else:
            if options['disable_cards']:
                self.disable_cards()
            if options['disable_whitelists']:
                self.disable_whitelists()
            if options['disable_extraordinary']:
                self.disable_extraordinary()

    def stdout_print(self, msg):
        if self.debug:
            self.stdout.write(msg)

    def disable_cards(self):
        PhoneUser.objects.all().update(enabled=False)
        self.stdout_print(
            'All cards disabled with success',
        )

    def disable_whitelists(self):
        Whitelist.objects.all().update(enabled=False)
        self.stdout_print(
            'All whitelists disabled with success',
        )

    def disable_extraordinary(self):
        Whitelist.objects.all().update(extraordinary=False)
        self.stdout_print(
            'All extraordinary permissione disabled with success',
        )



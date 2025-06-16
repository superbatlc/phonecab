from django.core.management.base import BaseCommand
from prefs.models import Pref

class Command(BaseCommand):
    help = 'Load default preferences into the Pref model'

    def handle(self, *args, **options):
        defaults = {
            'min_duration_with_credit': '10',
            'alert_before_end': '5',
            'enable_first_in': 'True',
            'ordinary_lawyer': 'False',
            'change_threshold': '15',
            'threshold': '600',
            'change_additional_calls': 'True',
            'default_additional_calls': '3',
            'max_calls_per_day': '10',
            'lawyer_call_limit': '5',
            'limit_additional_calls_per_day': '2',
            'covid_general': 'False',
            'limit_duration': '30',
            'header': 'Default Header',
        }

        for key, value in defaults.items():
            pref, created = Pref.objects.get_or_create(key=key, defaults={'value': value})
            if created:
                self.stdout.write(self.style.SUCCESS('Successfully created pref "%s"' % key))
            else:
                self.stdout.write(self.style.WARNING('Pref "%s" already exists' % key)) 
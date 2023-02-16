from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Fills User model with data from .csv files'

    def handle(self, *args, **options):
        print("CSV")

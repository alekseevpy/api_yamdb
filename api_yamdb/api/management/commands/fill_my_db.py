import csv
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Fills DB with data from .csv files"

    def handle(self, *args, **options):
        csv_root = settings.BASE_DIR / "static" / "data"
        print(csv_root)
        with open(csv_root / "users.csv", newline="") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",", quotechar="|")
            for row in csv_reader:
                print(", ".join(row))

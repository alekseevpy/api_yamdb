import csv
import sqlite3
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Fills DB with data from .csv files"

    def handle(self, *args, **options):
        csv_root: Path = settings.BASE_DIR / "static" / "data"
        files_paths = list(csv_root.glob("*.csv"))
        for file_path in files_paths:
            self.open_csv(file_path)

    @staticmethod
    def open_csv(file_path):
        with open(file_path, newline="") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",", quotechar="|")
            for row in csv_reader:
                print(", ".join(row))

    @staticmethod
    def write_to_db():
        con = sqlite3.connect(
            settings.BASE_DIR / "db.sqlite3"
        )  # change to 'sqlite:///your_filename.db'
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE t (col1, col2);"
        )  # use your column names here

        with open(
                'data.csv', 'r'
        ) as fin:  # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin)  # comma is default delimiter
            to_db = [(i['col1'], i['col2']) for i in dr]

        cur.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
        con.commit()
        con.close()
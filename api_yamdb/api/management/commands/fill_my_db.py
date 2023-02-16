import csv
import sqlite3
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Fills DB with data from .csv files"

    FILE_DB_TABLE: dict = {
        "category.csv": "reviews_category",
        "comments.csv": "reviews_comments",
        "genre.csv": "reviews_genre",
        "genre_title.csv": "reviews_genretitle",
        "review.csv": "reviews_review",
        "titles.csv": "reviews_titles",
        "users.csv": "users_user",
    }
    DB_PATH: Path = settings.DATABASES["default"]["NAME"]

    def handle(self, *args, **options):
        csv_root: Path = settings.BASE_DIR / "static" / "data"
        files_paths = list(csv_root.glob("*.csv"))

        print(self.DB_PATH)

        for file_path in files_paths:
            try:
                if file_path.name == "review.csv":
                    self.write_to_db(file_path)

            except Exception as er:
                print("тут", er)

    def write_to_db(self, file_path: Path) -> None:
        connection = sqlite3.connect(self.DB_PATH)
        cursor = connection.cursor()

        with open(file_path, newline="", encoding="utf-8") as csv_file:
            dict_reader = csv.DictReader(csv_file)
            to_db = [i for i in dict_reader]
        print(to_db.pop().keys())
        # cursor.executemany(
        #     """INSERT INTO t (col1, col2) VALUES (?, ?);""", to_db)
        # connection.commit()
        connection.close()

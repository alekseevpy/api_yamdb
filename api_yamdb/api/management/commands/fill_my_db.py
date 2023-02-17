import csv
import sqlite3
from pathlib import Path
import sys

from loguru import logger

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
        "titles.csv": "reviews_title",
        "users.csv": "users_user",
    }
    DB_PATH: Path = settings.DATABASES["default"]["NAME"]

    def handle(self, *args, **options):
        logger.debug("Starting...")

        csv_root: Path = settings.BASE_DIR / "static" / "data"
        files_paths = list(csv_root.glob("*.csv"))
        for file_path in files_paths:
            if file_path.name == "titles.csv":
                self.write_to_db(file_path)

        logger.debug("Finished!")

    def write_to_db(self, file_path: Path) -> None:
        try:
            logger.debug(f"Starting import from {file_path.name}")
            
            connection = sqlite3.connect(self.DB_PATH)
            cursor = connection.cursor()

            with open(file_path, newline="", encoding="utf-8") as csv_file:
                dict_reader = csv.DictReader(csv_file, quoting=csv.QUOTE_NONE)
                to_db = [i for i in dict_reader]

            table_keys = to_db[0].keys()
            values_query = self.make_values_query(table_keys)
            current_table = self.FILE_DB_TABLE[file_path.name]

            table_fields = ", ".join(table_keys)

            cursor.executemany(
                f"INSERT INTO {current_table}({table_fields}) VALUES ({values_query});",
                to_db,
            )
            connection.commit()
            logger.debug(f"Finished import from {file_path.name}")
        except Exception as er:
            logger.critical(f"Error: {er}")
        finally:
            connection.close()

    @staticmethod
    def make_values_query(table_keys: dict.keys) -> str:
        """Возвращает отформатированную строку.
        Пример: ":id, :username, :bio, :first_name, :last_name".
        """
        result = ""
        for key in table_keys:
            result += f":{key}, "
        return result[:-2]

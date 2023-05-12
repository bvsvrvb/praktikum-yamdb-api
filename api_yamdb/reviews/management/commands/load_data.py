import csv

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitleGenre, User)

IMPORT_ORDER = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    TitleGenre: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = "Заполняет БД из CSV"

    def handle(self, *args, **kwargs):
        for model, file_path in IMPORT_ORDER.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{file_path}',
                'r',
                encoding='utf-8'
            ) as f:
                reader = csv.DictReader(f)
                model.objects.bulk_create(model(**objs) for objs in reader)
                if model == TitleGenre:
                    with open(
                        f'{settings.BASE_DIR}/static/data/{file_path}',
                        'r',
                        encoding='utf-8'
                    ) as f1:
                        reader = csv.reader(f1)
                        for row in reader:
                            if reader.line_num == 1:
                                continue
                            title = Title.objects.get(id=row[1])
                            title.genre.add(row[2])
                        f.close()

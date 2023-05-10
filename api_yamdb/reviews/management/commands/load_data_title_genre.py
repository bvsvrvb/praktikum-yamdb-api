import os
import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import TitleGenre, Title


class Command(BaseCommand):
    help = "Заполняет БД из CSV"

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'static/data',
                                 'genre_title.csv')

        TitleGenre.objects.all().delete()

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if reader.line_num == 1:
                    continue
                title = Title.objects.get(id=row[1])
                title.genre.add(row[2])
            f.close()

        print('Данные успешно загружены')

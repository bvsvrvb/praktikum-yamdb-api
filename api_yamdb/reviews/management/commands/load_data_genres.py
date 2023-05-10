import os
import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Genre


class Command(BaseCommand):
    help = "Заполняет БД из CSV"

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'static/data',
                                 'genre.csv')

        Genre.objects.all().delete()

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            for row in reader:
                if reader.line_num == 1:
                    continue

                _, created = Genre.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2]
                )
            f.close()

        print('Данные успешно загружены')

import os
import csv

from django.conf import settings
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Title, Category


class Command(BaseCommand):
    help = "Заполняет БД из CSV"

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'static/data',
                                 'titles.csv')

        Title.objects.all().delete()

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            for row in reader:
                if reader.line_num == 1:
                    continue

                _, created = Title.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=get_object_or_404(Category, pk=row[3])
                )
            f.close()

        print('Данные успешно загружены')

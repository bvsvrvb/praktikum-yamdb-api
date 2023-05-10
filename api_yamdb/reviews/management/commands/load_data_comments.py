import os
import csv

from django.conf import settings
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Comment, Review, User


class Command(BaseCommand):
    help = "Заполняет БД из CSV"

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'static/data',
                                 'comments.csv')

        Comment.objects.all().delete()

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            for row in reader:
                if reader.line_num == 1:
                    continue

                _, created = Comment.objects.get_or_create(
                    id=row[0],
                    review=get_object_or_404(Review, pk=row[1]),
                    text=row[2],
                    author=get_object_or_404(User, pk=row[3]),
                    pub_date=row[4]
                )
            f.close()

        print('Данные успешно загружены')

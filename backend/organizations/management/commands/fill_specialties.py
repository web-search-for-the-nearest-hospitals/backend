import csv

from django.core.management.base import BaseCommand

from organizations.models import Specialty


class Command(BaseCommand):
    """Management-команда для заполнения информации
    о специальностях врачей из Приложения № 6 к приказу
    Минобрнауки России от 1312.2021 № 1229."""

    help = 'Заполнят БД сведениями о специальностях врачей'

    def add_arguments(self, parser):
        parser.add_argument('path',
                            type=str,
                            help=('Путь до файла'
                                  ' содержащего специальности врачей')
                            )

    def handle(self, *args, **options):
        file_path = options.get('path')
        with open(file_path, 'r') as f:
            reader_rows = csv.reader(f)
            specialties = [
                Specialty(code=row[0].replace('.', '-'),
                          name=row[1],
                          skill=row[2])
                for row in reader_rows
            ]
        Specialty.objects.bulk_create(specialties)

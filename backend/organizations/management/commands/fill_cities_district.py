import csv

from django.core.management.base import BaseCommand

from organizations.models import Town, District


class Command(BaseCommand):
    """Management-команда для заполнения информации
    о городах и районах."""

    help = 'Заполнят БД сведениями о специальностях врачей'

    def add_arguments(self, parser):
        parser.add_argument('path',
                            type=str,
                            help=('Путь до файла'
                                  ' содержащего данные городов и районов')
                            )

    def handle(self, *args, **options):
        file_path = options.get('path')
        with open(file_path, 'r') as f:
            reader_rows = csv.reader(f)
            new_districts = []
            new_towns = []
            for row in reader_rows:
                town = Town(name=row[0],
                            latitude=row[1],
                            longitude=row[2])
                new_towns.append(town)
                districts = row[3]

                for district in districts.split(';'):
                    new_district = District(name=district,
                                            town=town)
                    new_districts.append(new_district)
        Town.objects.bulk_create(new_towns)
        District.objects.bulk_create(new_districts)

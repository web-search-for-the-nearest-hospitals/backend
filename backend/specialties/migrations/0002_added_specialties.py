import csv
import re

from django.db import migrations

pattern: re.Pattern = re.compile(r'[Вв]рач-')


def shorten_doctor_spec(spec: str) -> str:
    return re.sub(pattern, '', spec).capitalize()


def fill_specialties(apps, schema_editor):
    """Заполняет информацию о специальностях врачей из
    Приложения № 6 к приказу Минобрнауки России от 1312.2021 № 1229."""

    Specialty = apps.get_model("specialties", "Specialty")
    with open('specialties/data/specialties.csv', 'r') as f:
        reader_rows = csv.reader(f)
        specialties = [
            Specialty(code=row[0].replace('.', '-'),
                      name=row[1],
                      skill=shorten_doctor_spec(row[2]))
            for row in reader_rows
        ]
    Specialty.objects.bulk_create(specialties)


def drop_specialties(apps, schema_editor):
    """Удаляет информацию о специальностях врачей."""

    Specialty = apps.get_model("specialties", "Specialty")
    Specialty.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('specialties', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=fill_specialties,
            reverse_code=drop_specialties),
    ]

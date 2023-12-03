from django.contrib.postgres import fields
from django.db import models

from .organization import Organization
from .specialty import Specialty


class OrganizationSpecialty(models.Model):
    """Расписание специальностей в больничке."""

    DAYS_OF_WEEK = (
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресение'),
    )
    DAY_TYPES = (
        ('weekday', 'выходной'),
        ('holiday', 'праздник'),
        ('daily', 'будни')
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='specialties'
    )
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.CASCADE,
        related_name='organizations'
    )

    day_of_the_week = models.PositiveIntegerField(
        'День недели',
        choices=DAYS_OF_WEEK
    )
    working_hours = fields.ArrayField(
        fields.ArrayField(
            models.CharField(
                max_length=5
            ),
            size=2
        ),
        verbose_name='Часы работы'
    )
    day_type = models.CharField(
        'Тип дня',
        max_length=30,
        choices=DAY_TYPES
    )

    def __str__(self):
        return (f'<Больничка {self.organization.name} + Специальность '
                f'{self.specialty.name}>')

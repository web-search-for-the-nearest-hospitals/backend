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

    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        on_delete=models.CASCADE,
        related_name='specialties'
    )
    specialty = models.ForeignKey(
        Specialty,
        verbose_name='Специальность',
        on_delete=models.CASCADE,
        related_name='organizations'
    )

    day_of_the_week = models.PositiveIntegerField(
        'День недели',
        choices=DAYS_OF_WEEK
    )
    working_hours = fields.ArrayField(
        models.CharField(
            max_length=11
        ),
        verbose_name='Часы работы'
    )

    class Meta:
        ordering = None
        verbose_name = 'Расписание специальностей'
        verbose_name_plural = 'Расписания специальностей'
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'specialty', 'day_of_the_week'],
                name='unique_orgspec_organization_specialty_day')
        ]

    def __str__(self):
        return (f'<Организация {self.organization.short_name} + Специальность '
                f'{self.specialty.name}>')

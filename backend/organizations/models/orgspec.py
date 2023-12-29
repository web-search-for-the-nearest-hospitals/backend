from django.db import models

from .organization import Organization
from .specialty import Specialty


class MyModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('specialty')


class OrganizationSpecialty(models.Model):
    """Расписание специальностей в больничке."""

    _base_manager = MyModelManager
    objects = MyModelManager()

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

    from_hour = models.TimeField(
        "Время начала работы",
        help_text='Время начала работы врача')

    to_hour = models.TimeField(
        'Время окончания работы',
        help_text='Время окончания работы врача')

    class Meta:
        ordering = None
        verbose_name = 'Расписание специальностей'
        verbose_name_plural = 'Расписания специальностей'
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'specialty', 'day_of_the_week'],
                name='organizations_unique_orgspec_schedule')
        ]

    def __str__(self):
        return (f'<Организация {self.organization} + Специальность '
                f'{self.specialty}>')

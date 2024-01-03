from django.conf import settings
from django.db import models

from .organization import Organization
from .specialty import Specialty


class Appointment(models.Model):
    """Запись к специальности врача в организации."""

    STATUSES = (
        ('free', 'Свободна'),
        ('planned', 'Запланирована'),
        ('confirmed', 'Подтверждена'),
        ('canceled', 'Отменена'),
        ('finished', 'Завершена'),
    )

    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    specialty = models.ForeignKey(
        Specialty,
        verbose_name='Специальность врача',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Клиент',
        on_delete=models.CASCADE,
        related_name='appointments',
        null=True, blank=True
    )

    datetime_created = models.DateTimeField(
        verbose_name='Дата и время создания записи пациента',
        auto_now=True,
        help_text='Дата и время создания записи пациента'
    )

    datetime_start = models.DateTimeField(
        verbose_name='Дата и время начала записи пациента',
        help_text='Дата и время начала записи пациента'
    )

    status = models.CharField(
        verbose_name='Статус записи',
        choices=STATUSES,
        default='free',
        help_text='Статус записи'
    )

    class Meta:
        ordering = ('datetime_start',)
        verbose_name = 'Запись пациента на прием'
        verbose_name_plural = 'Записи пациентов на прием'
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'specialty', 'datetime_start'],
                name='appointments_unique_org_spec_datetimestart')
        ]

    def __str__(self):
        return (f'<Запись к {self.specialty} в {self.organization} на '
                f'{self.datetime_start.strftime("%H:%M %d.%m.%Y")}>')

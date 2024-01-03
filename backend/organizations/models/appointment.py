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
        on_delete=models.SET_NULL,
        related_name='appointments',
        null=True
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Клиент',
        on_delete=models.CASCADE,
        related_name='appointments'
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

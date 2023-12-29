from django.conf import settings
from django.db import models

from .organization import Organization
from .specialty import Specialty


class Appointment(models.Model):
    """Запись к специальности врача в организации."""

    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    specialty = models.ForeignKey(
        Specialty,
        verbose_name='Специальность',
        on_delete=models.SET_NULL,
        related_name='appointments'
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Клиент',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    datetime_created = models.DateTimeField(
        'Дата создания записи к врачу в БД',
        auto_now=True,
        help_text='Дата создания записи к врачу в в БД')

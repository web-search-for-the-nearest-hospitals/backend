import uuid

from django.db import models

from .district import District
from .town import Town


class Organization(models.Model):
    """Описание модели организации."""

    id = models.BigAutoField(
        primary_key=True,
        help_text='Идентификатор организации в БД')

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text='Уникальный идентификатор организации')

    short_name = models.CharField(
        'Наименование',
        null=False,
        blank=False,
        help_text='Наименование организации',
        max_length=250)

    factual_address = models.CharField(
        'Адрес',
        help_text='Адрес местонахождения организации',
        max_length=250)

    date_added = models.DateTimeField(
        'Дата создания организации в БД',
        auto_now=True,
        help_text='Дата внесения организации в БД')

    longitude = models.FloatField(
        verbose_name='Долгота',
        help_text='Долгота расположения '
                  'организации',
        null=False, blank=False)

    latitude = models.FloatField(
        verbose_name='Широта',
        help_text='Широта расположения '
                  'организации',
        null=False, blank=False)

    site = models.CharField(
        'Сайт организации',
        max_length=100,
        null=True,
        blank=True,
        help_text='Сайт организации'
    )

    phone = models.CharField(
        'Номер телефона',
        max_length=18,
        null=True,
        blank=True,
        help_text='Телефон организации'
    )

    is_gov = models.BooleanField(
        'Государственная?',
        default=False,
        help_text='Является ли организация государственной'
    )

    is_full_time = models.BooleanField(
        'Круглосуточная?',
        default=False,
        help_text='Является ли организация круглосуточной'
    )

    about = models.TextField(
        'Дополнительная информация',
        null=True,
        blank=True,
        help_text='Дополнительная информация об организации'
    )
    town = models.ForeignKey(
        Town,
        on_delete=models.SET_NULL,
        verbose_name='Город организации',
        null=True,
        related_name='organizations',
        help_text='Город организации'
    )

    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        verbose_name='Район организации',
        null=True,
        related_name='organizations',
        help_text='Район организации'
    )

    class Meta:
        ordering = None
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        constraints = [
            models.UniqueConstraint(
                fields=("short_name", "factual_address"),
                name="unique_organization_short_name_factual_address")
        ]
        indexes = [
            models.Index(fields=['short_name', 'factual_address'])
        ]

    def __str__(self):
        return f'<Организация {self.short_name}>'

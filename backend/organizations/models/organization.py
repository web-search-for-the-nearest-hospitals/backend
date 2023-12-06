from django.db import models

from .town import Town


class Organization(models.Model):
    """Описание модели организации."""

    id = models.BigAutoField(
        primary_key=True,
        help_text='Идентификатор организации в БД')

    full_name = models.TextField(
        'Полное наименование',
        null=False,
        blank=False,
        help_text='Полное наименование организации')

    short_name = models.TextField(
        'Сокращенное наименование',
        null=True,
        blank=True,
        help_text='Сокращенное наименование организации')

    inn = models.CharField(
        'ИНН',
        max_length=12,
        null=True,
        blank=True,
        help_text='ИНН организации')

    factual_address = models.TextField(
        'Адрес',
        help_text='Адрес местонахождения организации')

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

    email = models.EmailField(
        'E-mail организации',
        max_length=100,
        null=True,
        blank=True,
        help_text='E-mail организации')

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

    town = models.OneToOneField(
        Town,
        on_delete=models.SET_NULL,
        verbose_name='Город организации',
        null=True
    )

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return f'<Организация {self.full_name}>'

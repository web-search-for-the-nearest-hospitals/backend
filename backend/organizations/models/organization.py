from django.db import models


class Organization(models.Model):
    """Описание модели организации."""

    id = models.BigAutoField(primary_key=True,
                             help_text='Идентификатор организации в БД')

    full_name = models.TextField('Полное наименование',
                                 null=False, blank=False,
                                 help_text='Полное наименование организации')
    short_name = models.TextField(
        'Сокращенное наименование',
        null=True, blank=True,
        help_text='Сокращенное наименование организации')
    inn = models.CharField('ИНН', max_length=12,
                           null=True, blank=True,
                           db_index=True,
                           help_text='ИНН организации')

    factual_address = models.TextField(
        'Адрес',
        help_text='Адрес местонахождения организации')
    region_code = models.CharField(
        'Код региона', max_length=3,
        null=True,
        help_text='Код региона в соответствии со справочником ФНС России')
    date_added = models.DateTimeField(
        auto_now=True,
        help_text='Дата внесения организации в БД')

    longitude = models.FloatField(verbose_name='Долгота',
                                  help_text='Долгота расположения организации')
    latitude = models.FloatField(verbose_name='Широта',
                                 help_text='Широта расположения организации')
    site = models.CharField(
        'Сайт организации', max_length=100,
        null=True,
        help_text='Сайт организации'
    )

    email = models.EmailField(
        'E-mail организации',
        max_length=100,
        null=True,
        help_text='E-mail организации')
    """
    specialities = models.ManyToManyField(Specialty,
                                          verbose_name='Специальности',
                                          related_name='organizations')
    """

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return f'<{self.full_name} ИНН {self.inn}>'

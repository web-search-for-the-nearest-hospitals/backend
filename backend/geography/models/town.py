from django.db import models


class Town(models.Model):
    """Описание модели города."""

    MAX_DIST = 25

    name = models.CharField(
        'Наименование города',
        help_text='Наименование города',
        max_length=25)

    longitude = models.FloatField(
        verbose_name='Долгота',
        help_text='Долгота расположения центра '
                  'города',
        null=False, blank=False)

    latitude = models.FloatField(
        verbose_name='Широта',
        help_text='Широта расположения центра '
                  'города',
        null=False, blank=False
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return f'<Город {self.name}>'

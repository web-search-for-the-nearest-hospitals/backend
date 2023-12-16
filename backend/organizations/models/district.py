from django.db import models

from .town import Town


class District(models.Model):
    """Описание модели района."""

    name = models.CharField(
        'Наименование района',
        help_text='Наименование района',
        max_length=40)

    town = models.ForeignKey(
        Town,
        on_delete=models.CASCADE,
        verbose_name='Город',
        null=True,
        related_name='districts',
        help_text='Город'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'

    def __str__(self):
        return f'<Район {self.name}>'

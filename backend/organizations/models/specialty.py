from django.db import models


class Specialty(models.Model):
    """Описание модели специальности врача."""

    code = models.CharField(
        'Код', max_length=8, primary_key=True,
        help_text='Код специальности'
    )
    name = models.CharField(
        'Наименование', max_length=150,
        help_text='Наименование специальности'
    )
    skill = models.CharField(
        'Врач', max_length=150,
        help_text='Наименование врача по специальности'
    )

    class Meta:
        ordering = ['skill']
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    def __str__(self):
        return f'<Специальность {self.skill}>'

from django.db import models


class Specialty(models.Model):
    """Описание модели специальности врача."""

    code = models.CharField('Код', max_length=8, primary_key=True)
    name = models.CharField('Наименование', max_length=150)
    skill = models.CharField('Врач', max_length=150)

    class Meta:
        ordering = ['code']
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    def __str__(self):
        return f'<Специальность {self.code} ({self.name})>'

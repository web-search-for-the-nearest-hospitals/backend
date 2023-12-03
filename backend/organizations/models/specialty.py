from django.db import models


class Specialty(models.Model):
    """Описание модели специальности врача.
    # https://base.garant.ru/70480868/7dede6ac8f25be619ed07c17ed1c62c9/
    """

    code = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=150)
    skill = models.CharField(max_length=150)

    class Meta:
        ordering = ['code']
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    def __str__(self):
        return f'<Специальность {self.code} ({self.name})>'

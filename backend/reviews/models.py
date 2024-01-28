from django.db import models

from organizations.models import Organization
from user.models import User


class Review(models.Model):
    CHOICES = [(i, i) for i in range(1, 6)]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name='Организация',
        related_name='reviews',
    )

    text = models.CharField(
        'Текст отзыва',
        max_length=500
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    score = models.IntegerField(
        'Оценка организации',
        choices=CHOICES,
    )

    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text

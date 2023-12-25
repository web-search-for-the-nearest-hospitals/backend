from django.db import models

from .organization import Organization


class OrganizationBusinessHour(models.Model):
    """Расписание работы организаций."""

    DAYS_OF_WEEK = (
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресение'),
    )
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        on_delete=models.CASCADE,
        related_name='business_hours',
    )

    day = models.IntegerField(
        'Номер дня недели',
        choices=DAYS_OF_WEEK,
        help_text='Номер дня недели')

    from_hour = models.TimeField(
        "Время начала работы",
        help_text='Время начала работы организации')

    to_hour = models.TimeField(
        'Время окончания работы',
        help_text='Время окончания работы организации')

    class Meta:
        ordering = None
        verbose_name = 'Рабочие часы организации'
        verbose_name_plural = 'Рабочие часы организаций'
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "day"),
                name="unique_org_day")
        ]

    def __str__(self) -> str:
        return (f'<День № {self.day}: {self.from_hour.strftime("%H:%M")}'
                f'-{self.to_hour.strftime("%H:%M")}>')

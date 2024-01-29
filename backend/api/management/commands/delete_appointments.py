import datetime

from django.core.management.base import BaseCommand

from appointments.models import Appointment


class Command(BaseCommand):
    """
    Management-команда для удаления из БД
    неиспользованные талоны на запись к врачу.
    """

    help = 'Удалят из БД неиспользованные талоны'

    def handle(self, *args, **options):
        Appointment.objects.filter(
            status=Appointment.FREE,
            client=None,
            datetime_start__date__lt=datetime.date.today()
        ).delete()

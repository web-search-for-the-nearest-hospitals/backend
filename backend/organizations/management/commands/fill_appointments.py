import datetime as dt

from django.core.management.base import BaseCommand
from django.utils import timezone

from organizations.models import Appointment, OrganizationSpecialty


class Command(BaseCommand):
    """
    Management-команда для заполнения БД
    свободными талонами записи к врачу.
    """

    help = 'Заполнят БД свободными талонами'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--num-days',
                            type=int,
                            choices=range(1, 9),
                            metavar="[1-8]",
                            default=8,
                            dest='N',
                            help=('Количество дней вперед от текущей даты,'
                                  'на которые нужно сформировать талоны.'
                                  ' (по умолчанию 8)')
                            )

        parser.add_argument('-d', '--duration',
                            type=int,
                            choices=range(12, 61),
                            metavar="[12-60]",
                            default=30,
                            dest='D',
                            help=('Длительность одного приема врача (в '
                                  'минутах). (по умолчанию: 30)')
                            )

    def handle(self, *args, **options):
        days = options.get('N')
        duration = options.get('D')
        appointments = []
        start_date = dt.date.today() + dt.timedelta(days=1)
        x_dates = [start_date + dt.timedelta(days=i) for i in range(days)]

        schedules = (
            OrganizationSpecialty
            .objects
            .only('day_of_the_week',
                  'from_hour',
                  'to_hour',
                  'organization',
                  'specialty')
            .values_list('day_of_the_week',
                         'from_hour',
                         'to_hour',
                         'organization',
                         'specialty',
                         named=True)
        )

        for schedule in schedules:

            for x_date in x_dates:

                num_day = x_date.weekday() + 1
                if num_day == schedule.day_of_the_week:
                    from_hour = schedule.from_hour

                    while from_hour < schedule.to_hour:
                        datetime_start = dt.datetime.combine(
                            x_date, from_hour)
                        datetime_start = timezone.make_aware(
                            datetime_start,
                            timezone=timezone.get_current_timezone())
                        appointments.append(
                            Appointment(
                                datetime_start=datetime_start,
                                organization_id=schedule.organization,
                                specialty_id=schedule.specialty,
                            )
                        )
                        temp_date_time = dt.datetime.combine(
                            start_date,
                            from_hour)
                        temp_date_time += dt.timedelta(minutes=duration)
                        from_hour = temp_date_time.time()

        Appointment.objects.bulk_create(appointments)

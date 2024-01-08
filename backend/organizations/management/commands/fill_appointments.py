from django.core.management.base import BaseCommand

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
                            choices=range(1, 16),
                            metavar="[1-15]",
                            default=15,
                            dest='N',
                            help=('Количество дней вперед от текущей даты,'
                                  'на которые нужно сформировать талоны.'
                                  ' (по умолчанию 15)')
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
        # Appointments,
        schedules = OrganizationSpecialty.objects.all()
        print(schedules)
        appointments = Appointment.objects.all()
        print(appointments)

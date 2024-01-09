import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0004_added_index_org_short_name_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(
                    auto_now=True,
                    help_text='Дата и время создания записи пациента',
                    verbose_name='Дата и время создания записи пациента')),
                ('datetime_start', models.DateTimeField(
                    help_text='Дата и время начала записи пациента',
                    verbose_name='Дата и время начала записи пациента')),
                ('status', models.CharField(
                    choices=[('free', 'Свободна'), ('planned', 'Запланирована'),
                             ('confirmed', 'Подтверждена'),
                             ('canceled', 'Отменена'),
                             ('finished', 'Завершена')], default='free',
                    help_text='Статус записи', verbose_name='Статус записи')),
                ('client', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='appointments',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Клиент')),
                ('organization',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='appointments',
                                   to='organizations.organization',
                                   verbose_name='Организация')),
                ('specialty',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='appointments',
                                   to='organizations.specialty',
                                   verbose_name='Специальность врача')),
            ],
            options={
                'verbose_name': 'Запись пациента на прием',
                'verbose_name_plural': 'Записи пациентов на прием',
                'ordering': ('datetime_start',),
            },
        ),
        migrations.AddConstraint(
            model_name='appointment',
            constraint=models.UniqueConstraint(
                fields=('organization', 'specialty', 'datetime_start'),
                name='appointments_unique_org_spec_datetimestart'),
        ),
    ]

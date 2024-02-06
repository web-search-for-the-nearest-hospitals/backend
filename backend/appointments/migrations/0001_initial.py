from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(help_text='Идентификатор талончика',
                                           primary_key=True, serialize=False)),
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
            ],
            options={
                'verbose_name': 'Запись пациента на прием',
                'verbose_name_plural': 'Записи пациентов на прием',
                'ordering': ('datetime_start',),
            },
        ),
    ]

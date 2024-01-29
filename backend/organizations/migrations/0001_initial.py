import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('geography', '0001_initial'),
        ('specialties', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id',
                 models.BigAutoField(
                     help_text='Идентификатор организации в БД',
                     primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(
                    default=uuid.uuid4, editable=False,
                    help_text='Уникальный идентификатор организации',
                    unique=True)),
                ('short_name',
                 models.CharField(help_text='Наименование организации',
                                  max_length=250, verbose_name='Наименование')),
                ('factual_address',
                 models.CharField(help_text='Адрес местонахождения организации',
                                  max_length=250, verbose_name='Адрес')),
                ('date_added', models.DateTimeField(
                    auto_now=True,
                    help_text='Дата внесения организации в БД',
                    verbose_name='Дата создания организации в БД')),
                ('longitude',
                 models.FloatField(help_text='Долгота расположения организации',
                                   verbose_name='Долгота')),
                ('latitude',
                 models.FloatField(help_text='Широта расположения организации',
                                   verbose_name='Широта')),
                ('site',
                 models.CharField(blank=True, help_text='Сайт организации',
                                  max_length=100, null=True,
                                  verbose_name='Сайт организации')),
                ('phone',
                 models.CharField(blank=True, help_text='Телефон организации',
                                  max_length=20, null=True,
                                  verbose_name='Номер телефона')),
                ('is_gov', models.BooleanField(
                    default=False,
                    help_text='Является ли организация государственной',
                    verbose_name='Государственная?')),
                ('is_full_time', models.BooleanField(
                    default=False,
                    help_text='Является ли организация круглосуточной',
                    verbose_name='Круглосуточная?')),
                ('about', models.TextField(
                    blank=True,
                    help_text='Дополнительная информация об организации',
                    max_length=500, null=True,
                    verbose_name='Дополнительная информация')),
                ('district',
                 models.ForeignKey(
                     help_text='Район организации', null=True,
                     on_delete=django.db.models.deletion.SET_NULL,
                     related_name='organizations',
                     to='geography.district',
                     verbose_name='Район организации')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
                'ordering': None,
            },
        ),
        migrations.CreateModel(
            name='OrganizationSpecialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('day_of_the_week', models.PositiveIntegerField(
                    choices=[(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'),
                             (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота'),
                             (7, 'Воскресение')], verbose_name='День недели')),
                ('from_hour',
                 models.TimeField(help_text='Время начала работы врача',
                                  verbose_name='Время начала работы')),
                ('to_hour',
                 models.TimeField(help_text='Время окончания работы врача',
                                  verbose_name='Время окончания работы')),
                ('organization',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='specialties',
                                   to='organizations.organization',
                                   verbose_name='Организация')),
                ('specialty',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='organizations',
                                   to='specialties.specialty',
                                   verbose_name='Специальность')),
            ],
            options={
                'verbose_name': 'Расписание специальностей',
                'verbose_name_plural': 'Расписания специальностей',
                'ordering': None,
            },
        ),
        migrations.CreateModel(
            name='OrganizationBusinessHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(
                    choices=[(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'),
                             (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота'),
                             (7, 'Воскресение')], help_text='Номер дня недели',
                    verbose_name='Номер дня недели')),
                ('from_hour',
                 models.TimeField(help_text='Время начала работы организации',
                                  verbose_name='Время начала работы')),
                ('to_hour', models.TimeField(
                    help_text='Время окончания работы организации',
                    verbose_name='Время окончания работы')),
                ('organization',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='business_hours',
                                   to='organizations.organization',
                                   verbose_name='Организация')),
            ],
            options={
                'verbose_name': 'Рабочие часы организации',
                'verbose_name_plural': 'Рабочие часы организаций',
                'ordering': None,
            },
        ),
    ]
